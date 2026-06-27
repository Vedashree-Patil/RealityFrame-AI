import cv2
import os 

class FrameManager:
    def __init__(self):
        self.frame = []
        self.folder = "frames"
        os.makedirs(self.folder, exist_ok = True)

    def capture(self, frame):
        self.frame.append(frame.copy())
        filename = f"memory_{len(self.frame):03d}.jpg"
        filepath = os.path.join(self.folder, filename)
        cv2.imwrite(filepath, frame)
        print(f"Saved frame to {filepath}")

    def get_frames(self):
        """Return the list of captured frames"""
        return self.frame
    
    def display_gallery(self, frame):

        thumbnail_width = 140
        thumbnail_height = 100
        spacing = 10

        for i, saved_frame in enumerate(self.frame):

            small = cv2.resize(saved_frame, (thumbnail_width, thumbnail_height))

            x = 10 + i * (thumbnail_width + spacing)
            y = 340

            if x + thumbnail_width > frame.shape[1]:
                break

            frame[y:y+thumbnail_height, x:x+thumbnail_width] = small

            cv2.rectangle(
                frame,
                (x-2, y-2),
                (x+thumbnail_width+2, y+thumbnail_height+2),
                (0,255,255),
                2
            )

            cv2.putText(
                frame,
                f"#{i+1}",
                (x+5, y-8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255,255,255),
                2
            )