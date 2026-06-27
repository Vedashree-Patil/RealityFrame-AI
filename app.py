import cv2
from modules.hand_tracker import HandTracker
from modules.frame_manager import FrameManager

# Initialize Hand Tracker
tracker = HandTracker()

# Store all captured frames
frame_manager = FrameManager()

# Open Camera
camera = cv2.VideoCapture(0)

while True:

    success, frame = camera.read()

    if not success:
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)
    clean_frame = frame.copy()

    # -------- Detect Hands --------
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

    # -------- Instructions --------
    cv2.putText(
        frame,
        "Press C = Capture | Press Q = Quit",
        (20, 460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2
    )

    # -------- Keyboard --------
    key = cv2.waitKey(1) & 0xFF

    if key == ord("c"):

        # Save a clean copy of the frame
        frame_manager.capture(clean_frame)

        print(f"Reality Frame {len(frame_manager.get_frames())} Captured!")

    # -------- Display all saved frames --------
    frame_manager.display_gallery(frame)

    # -------- Show Window --------
    cv2.imshow("RealityFrame AI", frame)

    # -------- Quit --------
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()