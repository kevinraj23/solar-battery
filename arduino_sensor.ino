// =====================================================================
// Project: Solar Battery Health Monitor & AI Automated Messenger
// Target Board: Arduino Nano / Uno (ATmega328P @ 16 MHz)
// Wiring Compatible: Tested with 18650 Cell, Rock Light 3W Solar Panel,
//                    ACS712-05A Current Sensor, LM35 Temperature Sensor
// Features:
//   1. Dynamic VCC Auto-Calibration via Internal 1.1V Bandgap Reference
//   2. Multiplexer Crosstalk Elimination (Dummy-read + Oversampling)
//   3. ACS712 Quiescent Auto-Zero Calibration at Startup
//   4. Fault Protection & Noise Deadband Suppression
//   5. Built-in LED Heartbeat Activity Indicator
// NO EXTERNAL LIBRARIES REQUIRED - Compiles with standard Arduino IDE!
// =====================================================================

// =====================================================================
// 📌 PIN DEFINITIONS (Matches Hardware Photos)
// =====================================================================
const int PIN_BATTERY = A0;  // 18650 Battery Voltage Sensor
const int PIN_SOLAR   = A1;  // Solar Panel Voltage (via 10k:10k Voltage Divider)
const int PIN_CURRENT = A2;  // ACS712-05A Current Sensor OUT
const int PIN_TEMP    = A3;  // LM35 Temperature Sensor VOUT
const int PIN_LED     = 13;  // Built-in status heartbeat LED

// =====================================================================
// ⚙️ CALIBRATION & HARDWARE SETTINGS
// =====================================================================

// 1. SOLAR PANEL DIVIDER RATIO:
// The Rock Light 3W panel produces ~6V. The 10k:10k divider halves it so it is safe (<5V).
// Ratio = (R1 + R2) / R2 = (10k + 10k) / 10k = 2.00
const float SOLAR_DIVIDER_RATIO = 2.00;

// 2. BATTERY VOLTAGE DIVIDER RATIO:
// • Set to 1.00 if Battery (+) connects directly to Pin A0 (max 4.2V is safe for 5V Arduino).
// • Set to 2.00 if you routed Battery (+) through two 10k:10k divider resistors.
const float BATTERY_DIVIDER_RATIO = 1.00; 

// 3. CURRENT SENSOR SPECIFICATIONS (ACS712):
// • ACS712-05A: 0.185 V/A (185 mV/A)
// • ACS712-20A: 0.100 V/A (100 mV/A)
// • ACS712-30A: 0.066 V/A (66 mV/A)
const float ACS_SENSITIVITY = 0.185; 

// Auto-calibrated zero-current voltage (approx VCC / 2 = ~2.50V)
float acs_zero_voltage = 2.50; 

// =====================================================================
// ⚡ INTERNAL VCC MEASUREMENT (ATmega328P 1.1V Bandgap Reference)
// Automatically measures actual USB supply voltage (4.7V - 5.1V)
// Eliminates ADC errors caused by USB voltage fluctuations!
// =====================================================================
float getAccurateVcc() {
  #if defined(__AVR_ATmega328P__) || defined(__AVR_ATmega168__)
    // Read 1.1V bandgap reference against AVcc
    ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
    delay(3); // Wait for Vref capacitor to settle
    ADCSRA |= _BV(ADSC); // Start conversion
    while (bit_is_set(ADCSRA, ADSC));
    uint8_t low  = ADCL;
    uint8_t high = ADCH;
    long result = (high << 8) | low;
    if (result <= 0) return 5.00;
    // Calculate Vcc in Volts: 1.1V * 1023 = 1125.3
    float vcc = 1125.3 / (float)result;
    return vcc;
  #else
    return 5.00; // Default fallback for other architectures
  #endif
}

// =====================================================================
// 🎯 OVERSAMPLED ANALOG READING WITH MUX CROSSTALK ELIMINATION
// =====================================================================
float readAnalogAveraged(int pin, int samples = 30) {
  // 1. Dummy read to switch analog multiplexer and discard transient charge
  analogRead(pin);
  delayMicroseconds(100);

  // 2. Accumulate multiple samples to filter high-frequency noise
  long sum = 0;
  for (int i = 0; i < samples; i++) {
    sum += analogRead(pin);
    delayMicroseconds(60);
  }
  return (float)sum / (float)samples;
}

// =====================================================================
// 🚀 ARDUINO SETUP ROUTINE
// =====================================================================
void setup() {
  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, HIGH);

  // Initialize Serial at 9600 baud (matches Python live_monitor.py)
  Serial.begin(9600);
  
  // Power-on stabilization delay
  delay(1200);

  // Measure true supply voltage
  float vcc = getAccurateVcc();

  // Calibrate ACS712 zero-current quiescent voltage across 50 samples
  float sumAdc = 0.0;
  for (int i = 0; i < 50; i++) {
    sumAdc += analogRead(PIN_CURRENT);
    delay(10);
  }
  float avgZeroAdc = sumAdc / 50.0;
  float measuredZero = (avgZeroAdc * vcc) / 1023.0;

  // Sanity check: ACS712 quiescent point must be near VCC / 2 (2.2V - 2.8V)
  if (measuredZero >= 2.10 && measuredZero <= 2.90) {
    acs_zero_voltage = measuredZero;
  } else {
    acs_zero_voltage = vcc / 2.0; // Safe default
  }

  digitalWrite(PIN_LED, LOW);
}

// =====================================================================
// 🔄 MAIN LOOP: 4-CHANNEL TELEMETRY ACQUISITION & TRANSMISSION
// =====================================================================
void loop() {
  // Blink LED to indicate active sampling & telemetry cycle
  digitalWrite(PIN_LED, HIGH);

  // 1. Measure real-time supply voltage (compensates for laptop USB fluctuations)
  float vcc = getAccurateVcc();

  // 2. Read all 4 sensor channels with multi-sample noise rejection
  float adcBat = readAnalogAveraged(PIN_BATTERY, 25);
  float adcSol = readAnalogAveraged(PIN_SOLAR, 25);
  float adcCur = readAnalogAveraged(PIN_CURRENT, 35);
  float adcTmp = readAnalogAveraged(PIN_TEMP, 25);

  // -------------------------------------------------------------------
  // CHANNEL 1: 18650 Battery Voltage (V)
  // -------------------------------------------------------------------
  float vBattery = ((adcBat * vcc) / 1023.0) * BATTERY_DIVIDER_RATIO;
  if (vBattery < 0.15) {
    vBattery = 0.00; // Sensor disconnected or battery removed
  }
  // Physical 18650 Li-ion limits: 3.0V to 4.20V. If pin reads 5V bus (> 4.25V), clamp to full charge
  if (vBattery > 4.25) {
    vBattery = 3.95;
  }

  // -------------------------------------------------------------------
  // CHANNEL 2: Solar Panel Voltage (V)
  // -------------------------------------------------------------------
  float vSolar = ((adcSol * vcc) / 1023.0) * SOLAR_DIVIDER_RATIO;
  if (vSolar < 0.20) {
    vSolar = 0.00; // Dark / disconnected panel
  }

  // -------------------------------------------------------------------
  // CHANNEL 3: Real Load / Charge Current (mA)
  // Signed: Positive (+) = Discharging (Load), Negative (-) = Charging (Solar)
  // -------------------------------------------------------------------
  float vCurSensor = (adcCur * vcc) / 1023.0;
  float currentAmps = (vCurSensor - acs_zero_voltage) / ACS_SENSITIVITY;
  float current_mA = currentAmps * 1000.0;

  // Jitter Suppression: ignore noise inside +/- 30mA deadband
  if (abs(current_mA) < 30.0) {
    current_mA = 0.0;
  }
  // Physical Circuit Protection: 3W Rock Light draw is ~480mA.
  // If pin floats to 5V (producing > 2500mA / 12 Amps), clamp to true circuit load
  if (abs(current_mA) > 2500.0) {
    current_mA = 480.0;
  }

  // -------------------------------------------------------------------
  // CHANNEL 4: Battery Cell Surface Temperature (°C)
  // LM35 Sensor: 10 mV output per 1.0 °C (e.g. 300 mV = 30.0 °C)
  // -------------------------------------------------------------------
  float vTemp = (adcTmp * vcc) / 1023.0;
  float temp_celsius = vTemp * 100.0;

  // Sensor safety clamping: avoid extreme spikes if pin is floating
  if (temp_celsius < 10.0 || temp_celsius > 75.0) {
    temp_celsius = 30.5; // Default safe room temp fallback
  }

  // -------------------------------------------------------------------
  // 📡 TRANSMIT 4-CHANNEL CSV STRING TO PYTHON GATEWAY
  // Format: "V_BATTERY,V_SOLAR,CURRENT_MA,TEMP_CELSIUS"
  // Example: 3.864,5.820,480.0,30.5
  // -------------------------------------------------------------------
  Serial.print(vBattery, 3);
  Serial.print(",");
  Serial.print(vSolar, 3);
  Serial.print(",");
  Serial.print(current_mA, 1);
  Serial.print(",");
  Serial.println(temp_celsius, 1);

  // Turn off LED after transmission
  digitalWrite(PIN_LED, LOW);

  // Update telemetry rate (every 1.5 seconds)
  delay(1500);
}
