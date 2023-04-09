//Written by Jason & Calder
#include <Servo.h>
Servo esc;
int escPin = 9; // PWM pin connected to the ESC signal wire
void setup() {
  Serial.begin(9600);
  esc.attach(escPin); // attach the servo object to the PWM pin
  Serial.print("step 1\n");
  delay(3000);
  esc.writeMicroseconds(1000);
  delay(2000);
  esc.writeMicroseconds(2000);
  delay(2000);
  int i = 1015;
  while(i<1700)
  {
      esc.writeMicroseconds(i);
      delay(1000);
      Serial.println(i);
      if(i>1300)
      {
        i += 25;
      }
      i += 25;
  }
  esc.writeMicroseconds(1700);
  delay(2000);
}
void loop() {
  // Set the speed of the motor to 100% throttle
  esc.writeMicroseconds(1700); // send a pulse with duration of 1.5 milliseconds (center position)
  delay(1000); // wait for 2 seconds
  Serial.print("loopy\n");
}
