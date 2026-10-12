// Solar Battery Health Monitor and Automated Messenger
// Edge Firmware for Arduino Nano (4-Channel Telemetry)
// Channels: Battery Voltage, Solar Voltage, Load Current, Cell Temperature

const int BATTERY_PIN = A0;  // 18650 Battery Voltage (via 10k protection resistor)
const int SOLAR_PIN   = A1;  // Solar Panel Voltage (via 10k:10k divider)
const int CURRENT_PIN = A2;  // ACS712-05A Current Sensor OUT
const int TEMP_PIN    = A3;  // LM35 Temperature Sensor VOUT

const float V_REF = 5.00;             // Arduino Nano 5.0V Logic
const float SOLAR_DIVIDER_RATIO = 2.0; // Two equal 10k resistors divide voltage by 2

// ACS712 5A Sensitivity: 185 mV per Ampere (0.185V/A)
// At 0A, output is V_REF / 2 = 2.50V (ADC ~ 512)
const float ACS_OFFSET_V = 2.50;
const float ACS_SENSITIVITY = 0.185; 

void setup() {
  Serial.begin(9600); // 9600 Baud Rate matches Python live_monitor.py
  delay(1000);
}

void loop() {
  // Average 15 samples to eliminate analog noise
  float rawBat = 0, rawSol = 0, rawCur = 0, rawTmp = 0;
  for(int i = 0; i < 15; i++) {
    rawBat += analogRead(BATTERY_PIN);
    rawSol += analogRead(SOLAR_PIN);
    rawCur += analogRead(CURRENT_PIN);
    rawTmp += analogRead(TEMP_PIN);
    delay(10);
  }
  rawBat /= 15.0;
  rawSol /= 15.0;
  rawCur /= 15.0;
  rawTmp /= 15.0;

  // 1. Voltages (V)
  float vBattery = (rawBat * V_REF) / 1024.0;
  float vSolar   = ((rawSol * V_REF) / 1024.0) * SOLAR_DIVIDER_RATIO;

  // 2. Load Current (mA) using ACS712
  float vSensorCur = (rawCur * V_REF) / 1024.0;
  float currentAmps = (vSensorCur - ACS_OFFSET_V) / ACS_SENSITIVITY;
  float current_mA = abs(currentAmps * 1000.0); // Absolute load current in mA

  // 3. Cell Temperature (°C) using LM35 (10 mV per °C)
  float vTemp = (rawTmp * V_REF) / 1024.0;
  float temp_celsius = vTemp * 100.0; // 0.1V = 10°C, 0.3V = 30°C

  // Transmit 4-Channel CSV to Python Gateway:
  // Format: "V_BATTERY,V_SOLAR,CURRENT_MA,TEMP_CELSIUS"
  Serial.print(vBattery, 3);
  Serial.print(",");
  Serial.print(vSolar, 3);
  Serial.print(",");
  Serial.print(current_mA, 1);
  Serial.print(",");
  Serial.println(temp_celsius, 1);

  delay(2000); // Send reading every 2 seconds
}
