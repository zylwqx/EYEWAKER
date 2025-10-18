const int leds[] = {4, 5, 6, 7, 8};
int buzzerPin = 9;
const int N = 5;
const unsigned long stepDelay = 1000; // ms between steps

void setup() {
  for (int i = 0; i < N; ++i) pinMode(leds[i], OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  tone(buzzerPin, 1000, 1000); // also halved duration here
}

void loop() {
  // Turn on one by one
  for (int i = 0; i < N; ++i) {
    digitalWrite(leds[i], HIGH);
    delay(stepDelay);
  }
  delay(1000); // hold all ON

  tone(buzzerPin, 587); // d
delay(125);

// Turn off one by one (reverse)
  for (int i = N - 1; i >= 0; --i) {
    digitalWrite(leds[i], LOW);
    delay(stepDelay);
  }
  delay(1000); // hold all OFF
}
