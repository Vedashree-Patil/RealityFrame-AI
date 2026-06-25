import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )

        self.drawer = mp.solutions.drawing_utils

    def detect_hands(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        hands = []

        if results.multi_hand_landmarks:

            for handNo, handLms in enumerate(results.multi_hand_landmarks):

                handedness = results.multi_handedness[
                    handNo
                ].classification[0].label

                self.drawer.draw_landmarks(
                    frame,
                    handLms,
                    self.mpHands.HAND_CONNECTIONS
                )

                landmark_list = []

                h, w, _ = frame.shape

                for idx, lm in enumerate(handLms.landmark):

                    cx = int(lm.x * w)
                    cy = int(lm.y * h)

                    landmark_list.append([idx, cx, cy])

                    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), cv2.FILLED)

                hands.append(
                    {
                        "type": handedness,
                        "landmarks": landmark_list
                    }
                )

        return frame, hands

    def count_fingers(self, hand):

        lm = hand["landmarks"]
        handType = hand["type"]

        fingers = []

        # ---------- THUMB ----------
        # Because webcam is flipped
        if handType == "Right":

            if lm[4][1] < lm[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        else:

            if lm[4][1] > lm[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # ---------- OTHER FINGERS ----------

        tipIds = [8, 12, 16, 20]

        for tip in tipIds:

            if lm[tip][2] < lm[tip - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers