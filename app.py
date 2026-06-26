import cv2
from modules.hand_tracker import HandTracker

# Initialize Hand Tracker
tracker = HandTracker()

# Variable to store captured Reality Frame
reality_frame = None

# Open Camera
camera = cv2.VideoCapture(0)

while True:

    success, frame = camera.read()

    if not success:
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)

    # Detect hands
    frame, hands = tracker.detect_hands(frame)

    # Count fingers
    if hands:
        for hand in hands:

            fingers = tracker.count_fingers(hand)
            total = fingers.count(1)

            # Information Panel
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
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Fingers : {total}",
                (35, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

    # Instructions
    cv2.putText(
        frame,
        "Press C = Capture | Press Q = Quit",
        (20, 460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2
    )

    # Keyboard Input
    key = cv2.waitKey(1) & 0xFF

    # Capture Reality Frame
    if key == ord("c"):
        reality_frame = frame.copy()

    # Draw Reality Frame
    if reality_frame is not None:

        # Resize
        small = cv2.resize(reality_frame, (220, 150))

        h, w = frame.shape[:2]

        x = w - 240
        y = 20

        frame[y:y+150, x:x+220] = small

        # Border
        cv2.rectangle(
            frame,
            (x - 2, y - 2),
            (x + 222, y + 152),
            (0, 255, 255),
            2
        )

        # Title
        cv2.putText(
            frame,
            "Reality Frame",
            (x, y + 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

    # Show Window
    cv2.imshow("RealityFrame AI", frame)

    # Quit
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()