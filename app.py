import cv2

from modules.hand_tracker import HandTracker

tracker = HandTracker()

camera = cv2.VideoCapture(0)

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame, hands = tracker.detect_hands(frame)

    if hands:

        for hand in hands:

            fingers = tracker.count_fingers(hand)

            total = fingers.count(1)

            cv2.rectangle(
                frame,
                (20, 20),
                (280, 110),
                (40, 40, 40),
                -1
            )

            cv2.putText(
                frame,
                f"Hand : {hand['type']}",
                (35, 55),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )

            cv2.putText(
                frame,
                f"Fingers : {total}",
                (35, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )

    cv2.imshow("RealityFrame AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()