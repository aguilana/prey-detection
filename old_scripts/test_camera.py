import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print(f"Error: Could not open camera.")
    exit()

print(f"press SPACE to caputure image, or Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print(f"Error: Could not read frame.")
        break

    cv2.imshow("Webcam preview", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        print(f"Quitting...")
        break
    elif key == ord(" "):
        cv2.imwrite("test_capture.jpg", frame)
        print(f"Image captured and saved as 'test_capture.jpg'")

cap.release()
cv2.destroyAllWindows()
