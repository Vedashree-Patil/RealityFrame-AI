import cv2
from modules.hand_tracker import HandTracker

camera = cv2.VideoCapture(0)

tracker = HandTracker()

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = tracker.detect_hands(frame)

    cv2.putText(
        frame,
        "RealityFrame AI",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow("RealityFrame AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()