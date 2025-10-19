"""
Simon Fraser University
Women in Engineering x Engineering Science Student Society Hackathon 2025

Dectector.py -- A program that uses OpenCV to detect whether a person's eyes are open or closed using a webcam feed.

Input: Webcam video feed.
Output: Visual display with rectangles around detected faces and eyes.

Author: Kevin Poon, Trevor Kwong, Max Leung, Bryan Servin. (Group 9)
"""

import cv2

face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
capture = cv2.VideoCapture(0)

while capture.isOpened():
    ret, image = capture.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert to grayscale for detection
    faces = face.detectMultiScale(gray, 1.3, 5) # Detect faces

    for (x, y, w, h) in faces: # Draw rectangle around face
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]

        eyes = eye.detectMultiScale(roi_gray, 1.3, 5)
        for (ex, ey, ew, eh) in eyes:
            eyes_detected = True
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    # Display the resulting image
    cv2.imshow('Face Detection', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()