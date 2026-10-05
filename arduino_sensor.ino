// Solar Battery Health Monitor and Automated Messenger
// Edge Firmware for Arduino Nano

const int BATTERY_PIN = A0;  // Reads 18650 Battery Voltage (via 10k protection resistor)
const int SOLAR_PIN   = A1;  // Reads Solar Panel Voltage (via 10k:10k voltage divider)

const float V_REF = 5.00;             // Arduino USB 5V logic
const float SOLAR_DIVIDER_RATIO = 2.0; // Two equal 10k resistors divide voltage by 2

void setup() {
  Serial.begin(9600); // 9600 Baud Rate matches Python
  delay(1000);
}

void loop() {
  // Average 10 samples to eliminate noise
  float rawBat = 0;
  float rawSol = 0;
  for(int i = 0; i < 10; i++) {
    rawBat += analogRead(BATTERY_PIN);
    rawSol += analogRead(SOLAR_PIN);
    delay(10);
  }
  rawBat /= 10.0;
  rawSol /= 10.0;

  // Convert ADC values (0-1023) to Volts
  float vBattery = (rawBat * V_REF) / 1024.0;
  float vSolar   = ((rawSol * V_REF) / 1024.0) * SOLAR_DIVIDER_RATIO;

  // Send formatted CSV line: "BATTERY_VOLTS,SOLAR_VOLTS"
  Serial.print(vBattery, 3);
  Serial.print(",");
  Serial.println(vSolar, 3);

  delay(2000); // Send reading every 2 seconds
}
