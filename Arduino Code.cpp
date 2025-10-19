/************************************************************************************
 * Simon Fraser University
 * Women in Engineering x Engineering Science Student Society Hackathon 2025
 * 
 * Project: Drowsiness Detection System
 * 
 * EyeDetector.py -- A program that uses OpenCV to detect whether a person's eyes are open or closed using a webcam feed.
 * 
 * Input: Webcam video feed.
 * 
 * Output: Visual display with rectangles around detected faces and eyes, text indicating eye state, and serial communication to an Arduino with the duration of eye closure.
 * 
 * Author: Kevin Poon, Trevor Kwong, Max Leung, Bryan Servin. (Group 9)
*************************************************************************************/

// Pins match your setup
const int leds[] = {4, 5, 6, 7, 8};
const int N = 5;
const int buzzerPin = 9;

// State
int lastCount = -1;// last value received from Python (0..5)
bool buzzedAtFive = false;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < N; ++i) pinMode(leds[i], OUTPUT); // LED pins as outputs
  pinMode(buzzerPin, OUTPUT); // Buzzer pin as output

}

void setBar(int count) {
  // Light "count" LEDs from left to right
  for (int i = 0; i < N; ++i) {
    digitalWrite(leds[i], (i < count) ? HIGH : LOW); // ON or OFF for each LED
  }
}

void loop() {
  // Read an integer line sent by Python like "3\n"
  if (Serial.available()) { // data available
    String line = Serial.readStringUntil('\n');  // non-blocking-ish with default timeout
    line.trim(); // remove whitespace
    if (line.length() > 0) { // got something
      int count = line.toInt();// if not a number -> 0
      if (count < 0) count = 0; 
      if (count > 5) count = 5;

      if (count != lastCount) {
        setBar(count); // Update LEDs

        // Handle buz when 5 logic (buzz once when we first hit 5)
        if (count == 5 && !buzzedAtFive) { // buzz once
          tone(buzzerPin, 1000, 5000); // 1kHz for 5 seconds
          buzzedAtFive = true; // mark that we've buzzed
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
