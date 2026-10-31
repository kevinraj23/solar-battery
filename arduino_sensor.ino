/*
  Solar Battery Health Monitor & AI Automated Messenger
  Upgraded: Dynamic Vcc Reference + Running-Load Safe Calibration
  
  Wiring:
    A0 -> Battery Voltage Divider (10k:10k)
    A1 -> ACS712 Current Sensor
    A2 -> LM35 Temperature Sensor
    A3 -> Solar Voltage Divider (10k:10k)
    Pin 13 -> Status LED
*/

const int VOLTAGE_PIN       = A0;  // Battery Voltage Divider (10k:10k)
const int CURRENT_PIN       = A1;  // ACS712 Current Sensor
const int TEMP_PIN          = A2;  // LM35 Temperature Sensor
const int SOLAR_VOLTAGE_PIN = A3;  // Solar Voltage Divider (10k:10k)
const int LED_PIN           = 13;

const float VOLTAGE_DIVIDER_RATIO       = 2.0;
const float SOLAR_VOLTAGE_DIVIDER_RATIO = 2.0;

// Check the chip text on your ACS712 module!
// Use 0.185 for -05B (5A), 0.100 for -20A (20A), or 0.066 for -30A (30A)
const float ACS712_SENSITIVITY = 0.185;

const int SAMPLES = 80;
float currentZeroOffsetRatio = 0.500; // Ratiometric midpoint (Vcc / 2)

// Measure actual Arduino Nano Vcc using internal 1.1V reference
float readSupplyVcc() {
  ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
  delay(3);
  ADCSRA |= _BV(ADSC);
  while (bit_is_set(ADCSRA, ADSC));
  long result = ADCL;
  result |= ADCH << 8;
  return 1125.300 / result; // Returns real Vcc in Volts (e.g., 4.72V on USB)
}

float readAverageADC(int pin) {
  analogRead(pin); // Discard first mux switch reading
  delay(2);
  long total = 0;
  for (int i = 0; i < SAMPLES; i++) {
    total += analogRead(pin);
    delayMicroseconds(500);
  }
  return total / (float)SAMPLES;
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  Serial.begin(9600);
  delay(1000);

  // Calibrate zero ratio ONLY if motor is truly off (~511.5 ADC +/- 5 counts)
  float bootADC = readAverageADC(CURRENT_PIN);
  float bootRatio = bootADC / 1023.0;
  if (bootRatio >= 0.495 && bootRatio <= 0.505) {
    currentZeroOffsetRatio = bootRatio;
  } else {
    currentZeroOffsetRatio = 0.500; // Motor is already spinning; use true Vcc/2
  }

  Serial.println("battery_voltage,current_amp,temperature_c,solar_voltage");
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  float vcc = readSupplyVcc();

  // 1. Battery voltage
  float batteryVoltage = ((readAverageADC(VOLTAGE_PIN) * vcc) / 1023.0) * VOLTAGE_DIVIDER_RATIO;
  if (batteryVoltage < 0.2) batteryVoltage = 0.0;

  // 2. ACS712 current (Amperes)
  float sensorVoltage = (readAverageADC(CURRENT_PIN) * vcc) / 1023.0;
  float zeroVoltage   = currentZeroOffsetRatio * vcc;
  float currentAmp    = fabs(sensorVoltage - zeroVoltage) / ACS712_SENSITIVITY;
  if (currentAmp < 0.015 || currentAmp > 15.0) currentAmp = 0.0; // Detects down to 15 mA

  // 3. LM35 temperature (C)
  float tempVoltage  = (readAverageADC(TEMP_PIN) * vcc) / 1023.0;
  float temperatureC = tempVoltage * 100.0;
  if (temperatureC < 5.0 || temperatureC > 85.0) temperatureC = 30.5;

  // 4. Solar panel voltage
  float solarVoltage = ((readAverageADC(SOLAR_VOLTAGE_PIN) * vcc) / 1023.0) * SOLAR_VOLTAGE_DIVIDER_RATIO;
  if (solarVoltage < 0.2) solarVoltage = 0.0;

  // 5. Send CSV over USB
  Serial.print(batteryVoltage, 3);
  Serial.print(",");
  Serial.print(currentAmp, 3);
  Serial.print(",");
  Serial.print(temperatureC, 2);
  Serial.print(",");
  Serial.println(solarVoltage, 3);

  digitalWrite(LED_PIN, LOW);
  delay(1500);
}
