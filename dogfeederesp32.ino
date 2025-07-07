#include <ESP32Servo.h>

#define TRIG_PIN 12     
#define ECHO_PIN 14     
#define LED_PIN 26      
#define SERVO_PIN 27    

Servo myServo;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  myServo.attach(SERVO_PIN);
}

void loop() {
  
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;  // Convert to cm

  
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();  

    if (data == "DOG_DETECTED" && distance < 20) {
      Serial.println("⚡ ESP32 Received: DOG_DETECTED");

      
      digitalWrite(LED_PIN, HIGH);
      delay(2000);
      digitalWrite(LED_PIN, LOW);

      
      for (int pos = 0; pos <= 180; pos++) {
        myServo.write(pos);
        delay(15);
      }
      for (int pos = 180; pos >= 0; pos--) {
        myServo.write(pos);
        delay(15);
      }
    }
  }

  delay(500); // Small delay between loop cycles
}
