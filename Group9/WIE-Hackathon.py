import cv2
import time
import serial

# Talking to Arduino
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)
time.sleep(2)

# Load Haar cascades for face and eye detection
face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
capture = cv2.VideoCapture(0)

closed_start = None # Variables to track eye state
CLOSED_THRESHOLD = 5.0  # seconds eyes must stay closed

last_sent_count = -1 # To avoid redundant serial messages

while capture.isOpened():
    ret, image = capture.read()
    if not ret:
        break
    
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert to grayscale for detection
    faces = face.detectMultiScale(gray, 1.3, 5) # Detect faces

    eyes_detected = False # Reset eye detection flag

    for (x, y, w, h) in faces: # Draw rectangle around face
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]

        eyes = eye.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
        for (ex, ey, ew, eh) in eyes:
            eyes_detected = True
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    if eyes_detected: # Check open/closed state
        closed_start = None
        cv2.putText(image, "Eyes Open", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        count = 0
    else:
        if closed_start is None:
            closed_start = time.time()
        duration = time.time() - closed_start
        count = int(duration)
        if count > 5:
            count = 5
        if duration > CLOSED_THRESHOLD:
            cv2.putText(image, "Eyes Closed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)    

    if count != last_sent_count: # Send count to Arduino if changed
        try:
            arduino.write(f"{count}\n".encode("utf-8")) # Send count as string
        except Exception as e:
            print(f"Error sending to Arduino: {e}")
        last_sent_count = count

    cv2.imshow("Face and Eye Detection", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()