import cv2

print("🔍 Scanning for available cameras...\n")

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✅ Camera index {i} is working.")
            cv2.imshow(f"Camera {i}", frame)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
        else:
            print(f"⚠️  Camera index {i} opened, but no frame.")
        cap.release()
    else:
        print(f"❌ Camera index {i} not available.")
