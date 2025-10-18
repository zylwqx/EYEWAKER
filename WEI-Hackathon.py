import cv2
import time as t

face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
capture = cv2.VideoCapture(0)

closed_start = None # Time when eyes were first detected as closed
Closed_Threshold = 5.0 # seconds eyes must be closed to trigger

while capture.isOpened():
    _, image = capture.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, 1.3, 5)

    eyes_detected = False

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]

        eyes = eye.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
        for (ex, ey, ew, eh) in eyes:
            eyes_detected = True
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    if eyes_detected:
        closed_start = None
        cv2.putText(image, "Eyes Open", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        if closed_start is None:
            closed_start = t.time()
            cv2
        elif t.time() - closed_start > Closed_Threshold:
            cv2.putText(image, "ALERT! Eyes Closed!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Eye State Detection', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()