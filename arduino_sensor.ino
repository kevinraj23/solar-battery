// =====================================================================
// Project: Solar Battery Health Monitor and Automated Messenger
// Platform: Arduino Nano / Uno (ATmega328P)
// Description: 4-Channel Precision Edge Telemetry Firmware
// NO EXTERNAL LIBRARIES REQUIRED - Compiles out of the box!
// =====================================================================

// Pin Definitions
const int PIN_BATTERY = A0;  // 18650 Battery Voltage (direct via 10k protection resistor)
const int PIN_SOLAR   = A1;  // Solar Panel Voltage (via 10k:10k voltage divider)
const int PIN_CURRENT = A2;  // ACS712-05A Current Sensor OUT
const int PIN_TEMP    = A3;  // LM35 Temperature Sensor VOUT
const int PIN_LED     = 13;  // Built-in status LED heartbeat

// Hardware Calibration Constants
const float V_REF = 5.00;              // Microcontroller operating voltage
const float SOLAR_DIVIDER_RATIO = 2.0; // Two equal 10k resistors divide voltage by 2
const float ACS_OFFSET_V = 2.50;       // ACS712 0A resting midpoint (VCC / 2)
const float ACS_SENSITIVITY = 0.185;   // ACS712-05A: 185 mV/A (0.185 V/A)

void setup() {
  pinMode(PIN_LED, OUTPUT);
  Serial.begin(9600); // 9600 Baud Rate matches Python live_monitor.py
  
  // Power-on stabilization delay
  delay(1000);
}

void loop() {
  // Blink LED to indicate active sampling & transmission
  digitalWrite(PIN_LED, HIGH);

  // Take 20 analog samples to average out high-frequency electrical noise
  float sumBat = 0.0, sumSol = 0.0, sumCur = 0.0, sumTmp = 0.0;
  const int NUM_SAMPLES = 20;

  for (int i = 0; i < NUM_SAMPLES; i++) {
    // Read each analog pin with a small settling delay between channels
    sumBat += analogRead(PIN_BATTERY);
    delayMicroseconds(200);
    sumSol += analogRead(PIN_SOLAR);
    delayMicroseconds(200);
    sumCur += analogRead(PIN_CURRENT);
    delayMicroseconds(200);
    sumTmp += analogRead(PIN_TEMP);
    delay(5);
  }

  // Calculate averaged analog ADC values (0 to 1023)
  float avgBat = sumBat / NUM_SAMPLES;
  float avgSol = sumSol / NUM_SAMPLES;
  float avgCur = sumCur / NUM_SAMPLES;
  float avgTmp = sumTmp / NUM_SAMPLES;

  // 1. Calculate 18650 Battery Voltage (V)
  float vBattery = (avgBat * V_REF) / 1023.0;

  // 2. Calculate Solar Panel Voltage (V)
  float vSolar = ((avgSol * V_REF) / 1023.0) * SOLAR_DIVIDER_RATIO;

  // 3. Calculate Real Load Current (mA) using ACS712
  float vCurSensor = (avgCur * V_REF) / 1023.0;
  float currentAmps = (vCurSensor - ACS_OFFSET_V) / ACS_SENSITIVITY;
  float current_mA = abs(currentAmps * 1000.0);
  
  // Noise deadband: suppress minor sensor jitter below 40mA when load is disconnected
  if (current_mA < 40.0) {
    current_mA = 0.0;
  }

  // 4. Calculate Cell Surface Temperature (°C) using LM35 (10 mV per °C)
  float vTemp = (avgTmp * V_REF) / 1023.0;
  float temp_celsius = vTemp * 100.0;

  // Transmit 4-Channel CSV string to Python Gateway
  // Format: "V_BATTERY,V_SOLAR,CURRENT_MA,TEMP_CELSIUS"
  Serial.print(vBattery, 3);
  Serial.print(",");
  Serial.print(vSolar, 3);
  Serial.print(",");
  Serial.print(current_mA, 1);
  Serial.print(",");
  Serial.println(temp_celsius, 1);

  // Turn off LED after transmission
  digitalWrite(PIN_LED, LOW);

  // Send update every 2 seconds
  delay(2000);
}
