import cv2
import os
import json
from datetime import datetime
from modules.gemini_ai import describe_image


class FrameManager:

    def __init__(self):

        # Store captured frames for gallery
        self.frames = []

        # Folder paths
        self.folder = "frames"
        self.memory_folder = "memories"

        # Create folders if they don't exist
        os.makedirs(self.folder, exist_ok=True)
        os.makedirs(self.memory_folder, exist_ok=True)

        # Load previously saved memories
        self.load_memories()

    def load_memories(self):

        print("📂 Loading saved memories...")

        self.frames = []

        for filename in os.listdir(self.memory_folder):

            if filename.endswith(".json"):

                json_path = os.path.join(self.memory_folder, filename)

                with open(json_path, "r") as file:
                    metadata = json.load(file)

                image_path = os.path.join(
                    self.folder,
                    metadata["filename"]
                )

                image = cv2.imread(image_path)

                # Skip if image is missing
                if image is None:
                    continue

                self.frames.append({
                    "image": image,
                    "filename": metadata["filename"],
                    "filepath": image_path,
                    "timestamp": metadata["timestamp"],
                    "description": metadata["description"],
                    "objects": metadata["objects"],
                    "tags": metadata["tags"]
                })

                print(f"Loaded {metadata['filename']}")

    def capture(self, frame):

        timestamp = datetime.now()

        filename = timestamp.strftime("%Y%m%d_%H%M%S") + ".jpg"

        filepath = os.path.join(self.folder, filename)

        # Save image
        cv2.imwrite(filepath, frame)

        print("🤖 Asking Gemini to analyze the image...")

        ai_result = describe_image(filepath)

        metadata = {
            "filename": filename,
            "timestamp": timestamp.strftime("%d-%m-%Y %H:%M:%S"),
            "description": ai_result["description"],
            "objects": ai_result["objects"],
            "tags": ai_result["tags"]
        }

        json_filename = filename.replace(".jpg", ".json")
        json_path = os.path.join(self.memory_folder, json_filename)

        # Save metadata
        with open(json_path, "w") as file:
            json.dump(metadata, file, indent=4)

        print(f"✅ Saved {filename}")
        print(f"✅ Saved metadata as {json_filename}")

        # Store for current session gallery
        self.frames.append({
            "image": frame.copy(),
            "filename": filename,
            "filepath": filepath,
            "timestamp": metadata["timestamp"],
            "description": metadata["description"],
            "objects": metadata["objects"],
            "tags": metadata["tags"]
        })

    def get_frames(self):
        return self.frames

    def display_gallery(self, frame):

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

            if x + thumbnail_width > frame.shape[1]:
                break

            frame[
                y:y + thumbnail_height,
                x:x + thumbnail_width
            ] = small

            cv2.rectangle(
                frame,
                (x - 2, y - 2),
                (x + thumbnail_width + 2,
                 y + thumbnail_height + 2),
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"#{i + 1}",
                (x + 5, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                memory["timestamp"].split(" ")[1],
                (x + 5, y + thumbnail_height + 18),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 255, 255),
                1
            )