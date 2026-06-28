import cv2
import os
import json
from datetime import datetime


class FrameManager:

    def __init__(self):

        # Store captured frames for gallery display
        self.frames = []

        # Folder to save captured images
        self.folder = "frames"
        os.makedirs(self.folder, exist_ok=True)

        # Folder to save metadata
        self.memory_folder = "memories"
        os.makedirs(self.memory_folder, exist_ok=True)

    def capture(self, frame):
        """
        Capture a frame, save the image,
        create metadata, and store it for the gallery.
        """

        timestamp = datetime.now()

        # Image filename
        filename = timestamp.strftime("%Y%m%d_%H%M%S") + ".jpg"

        filepath = os.path.join(self.folder, filename)

        # Save image
        cv2.imwrite(filepath, frame)

        # Metadata
        metadata = {
            "filename": filename,
            "timestamp": timestamp.strftime("%d-%m-%Y %H:%M:%S"),
            "description": "",
            "objects": [],
            "tags": []
        }

        # Save metadata as JSON
        json_filename = filename.replace(".jpg", ".json")
        json_path = os.path.join(self.memory_folder, json_filename)

        with open(json_path, "w") as file:
            json.dump(metadata, file, indent=4)

        # Store information for gallery display
        self.frames.append({
            "image": frame.copy(),
            "filename": filename,
            "filepath": filepath,
            "timestamp": timestamp.strftime("%d-%m-%Y %H:%M:%S")
        })

        print(f"✅ Saved {filename}")

    def get_frames(self):
        """Return all captured memories."""
        return self.frames

    def display_gallery(self, frame):
        """
        Display captured memories
        as thumbnails at the bottom.
        """

        thumbnail_width = 140
        thumbnail_height = 100
        spacing = 10

        for i, memory in enumerate(self.frames):

            small = cv2.resize(
                memory["image"],
                (thumbnail_width, thumbnail_height)
            )

            x = 10 + i * (thumbnail_width + spacing)
            y = 340

            # Stop drawing if thumbnails exceed window width
            if x + thumbnail_width > frame.shape[1]:
                break

            frame[
                y:y + thumbnail_height,
                x:x + thumbnail_width
            ] = small

            # Border
            cv2.rectangle(
                frame,
                (x - 2, y - 2),
                (x + thumbnail_width + 2, y + thumbnail_height + 2),
                (0, 255, 255),
                2
            )

            # Memory number
            cv2.putText(
                frame,
                f"#{i + 1}",
                (x + 5, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )

            # Timestamp
            cv2.putText(
                frame,
                memory["timestamp"].split(" ")[1],
                (x + 5, y + thumbnail_height + 18),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 255, 255),
                1
            )