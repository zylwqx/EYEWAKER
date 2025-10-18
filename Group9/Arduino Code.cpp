// Pins match your setup
const int leds[] = {4, 5, 6, 7, 8};
const int N = 5;
const int buzzerPin = 9;

// State
int lastCount = -1;      // last value received from Python (0..5)
bool buzzedAtFive = false;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < N; ++i) pinMode(leds[i], OUTPUT);
  pinMode(buzzerPin, OUTPUT);

}

void setBar(int count) {
  // Light "count" LEDs from left to right, others OFF
  for (int i = 0; i < N; ++i) {
    digitalWrite(leds[i], (i < count) ? HIGH : LOW);
  }
}

void loop() {
  // Read an integer line sent by Python like "3\n"
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');  // non-blocking-ish with default timeout
    line.trim();
    if (line.length() > 0) {
      int count = line.toInt();  // if not a number -> 0
      if (count < 0) count = 0;
      if (count > 5) count = 5;

      if (count != lastCount) {
        setBar(count);

        // Handle buzz-at-5 logic (buzz once when we first hit 5)
        if (count == 5 && !buzzedAtFive) {
          tone(buzzerPin, 1000, 5000); 
          buzzedAtFive = true;
        }
        if (count < 5) {
          // Reset so we can buzz again next time we reach 5
          buzzedAtFive = false;
        }

        lastCount = count;
      }
    }
  }

  // No delays needed; we react as new data arrives
}
