#include <Stepper.h>

// change pins and steps as needed
const int stepsPerRevolution = 2048;
Stepper stepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {
  Serial.begin(9600);
  stepper.setSpeed(5); // RPM
}

void loop() {
  if (Serial.available()) {
    char dir = Serial.read();

    if (dir == 'L') {
      stepper.step(+5);  // small left step
    }
    else if (dir == 'R') {
      stepper.step(-5);   // small right step
    }
    // Optionally stop or center on 'C'
  }
}
