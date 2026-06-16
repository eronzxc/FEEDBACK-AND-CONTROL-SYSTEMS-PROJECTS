#include <Servo.h>

// Configuration
const int SERVO_PIN = 9;
const long BAUD_RATE = 9600;

Servo myServo;

void setup() {
  Serial.begin(BAUD_RATE);
  myServo.attach(SERVO_PIN);
  
  // Initialize to a safe neutral position
  myServo.write(90);
  
  // Wait for serial port to connect
  while (!Serial) { ; }
}

void loop() {
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n');
    inputString.trim();

    if (inputString.length() > 0) {
      int angle = inputString.toInt();

      if (angle >= 0 && angle <= 180) {
        myServo.write(angle);
        Serial.print("SUCCESS: Angle set to ");
        Serial.println(angle);
      } else {
        Serial.print("ERROR: Invalid range (0-180). Received: ");
        Serial.println(angle);
      }
    }
  }
}