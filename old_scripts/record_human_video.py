import cv2
from datetime import datetime

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print(f"Error: Could not open camera.")
    exit()

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"videos/human/human_video_{timestamp}.mp4"
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter(output_file, fourcc, 20.0, (640, 480))
print(f"Recording video to {output_file}. Press 'q' to stop recording.")
while True:
    ret, frame = cap.read()

    if not ret:
        print(f"Error: Could not read frame.")
        break

    # Write the frame to the video file
    out.write(frame)
    # Display the frame
    cv2.imshow("Recording - Press q to stop", frame)

    # Check for user input
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print(f"Quitting...")
        break

cap.release()
out.release()
cv2.destroyAllWindows()
print(f"Video saved as {output_file}.")
