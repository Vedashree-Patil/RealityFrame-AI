import cv2
import os
import json
from datetime import datetime
from modules.gemini_ai import describe_image


class FrameManager:

    def __init__(self):

        self.frames = []

        self.folder = "frames"
        self.memory_folder = "memories"

        os.makedirs(self.folder, exist_ok=True)
        os.makedirs(self.memory_folder, exist_ok=True)

        self.load_memories()

    # -------------------------------------------------
    # Load all memories from disk
    # -------------------------------------------------

    def load_memories(self):

        print("Loading saved memories...")

        self.frames.clear()

        json_files = sorted(
            os.listdir(self.memory_folder),
            reverse=True
        )

        for filename in json_files:

            if not filename.endswith(".json"):
                continue

            json_path = os.path.join(
                self.memory_folder,
                filename
            )

            try:

                with open(json_path, "r") as file:

                    metadata = json.load(file)

            except Exception as e:

                print(f"Error reading {filename}: {e}")
                continue

            image_path = os.path.join(
                self.folder,
                metadata["filename"]
            )

            if not os.path.exists(image_path):
                continue

            image = cv2.imread(image_path)

            if image is None:
                continue

            self.frames.append({

                "image": image,
                "filename": metadata.get("filename"),
                "filepath": image_path,
                "timestamp": metadata.get("timestamp", ""),
                "description": metadata.get("description", ""),
                "objects": metadata.get("objects", []),
                "tags": metadata.get("tags", []),
                "favorite": metadata.get("favorite", False)

            })

            print(f"Loaded {metadata['filename']}")

        print(f"Loaded {len(self.frames)} memories.")

    # -------------------------------------------------
    # Capture Memory
    # -------------------------------------------------

    def capture(self, frame):

        timestamp = datetime.now()

        filename = timestamp.strftime(
            "%Y%m%d_%H%M%S"
        ) + ".jpg"

        filepath = os.path.join(
            self.folder,
            filename
        )

        cv2.imwrite(filepath, frame)

        print("Asking Gemini AI...")

        ai_result = describe_image(filepath)

        metadata = {

            "filename": filename,

            "timestamp":
            timestamp.strftime("%d-%m-%Y %H:%M:%S"),

            "description":
            ai_result.get(
                "description",
                ""
            ),

            "objects":
            ai_result.get(
                "objects",
                []
            ),

            "tags":
            ai_result.get(
                "tags",
                []
            ),

            "favorite": False

        }

        json_name = filename.replace(
            ".jpg",
            ".json"
        )

        json_path = os.path.join(
            self.memory_folder,
            json_name
        )

        with open(json_path, "w") as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

        self.frames.insert(0, {

            "image": frame.copy(),

            "filename": filename,

            "filepath": filepath,

            "timestamp":
            metadata["timestamp"],

            "description":
            metadata["description"],

            "objects":
            metadata["objects"],

            "tags":
            metadata["tags"],

            "favorite": False

        })

        print(f"Memory saved -> {filename}")
            # -------------------------------------------------
    # Return all memories
    # -------------------------------------------------

    def get_frames(self):
        return self.frames

    # -------------------------------------------------
    # Get one memory
    # -------------------------------------------------

    def get_memory(self, index):

        if 0 <= index < len(self.frames):
            return self.frames[index]

        return None

    # -------------------------------------------------
    # Get all favorite memories
    # -------------------------------------------------

    def get_favorites(self):

        return [
            memory
            for memory in self.frames
            if memory["favorite"]
        ]

    # -------------------------------------------------
    # Search memories
    # -------------------------------------------------

    def search_memories(self, query):

        query = query.lower().strip()

        results = []

        for memory in self.frames:

            searchable_text = " ".join([

                memory["filename"],
                memory["description"],
                " ".join(memory["objects"]),
                " ".join(memory["tags"])

            ]).lower()

            if query in searchable_text:
                results.append(memory)

        return results

    # -------------------------------------------------
    # Delete Memory
    # -------------------------------------------------

    def delete_memory(self, index):

        if index < 0 or index >= len(self.frames):
            return False

        memory = self.frames[index]

        # Delete image
        if os.path.exists(memory["filepath"]):
            os.remove(memory["filepath"])

        # Delete JSON
        json_file = memory["filename"].replace(
            ".jpg",
            ".json"
        )

        json_path = os.path.join(
            self.memory_folder,
            json_file
        )

        if os.path.exists(json_path):
            os.remove(json_path)

        # Remove from memory list
        self.frames.pop(index)

        print(f"Deleted {memory['filename']}")

        return True

    # -------------------------------------------------
    # Toggle Favorite
    # -------------------------------------------------

    def toggle_favorite(self, index):

        if index < 0 or index >= len(self.frames):
            return False

        memory = self.frames[index]

        memory["favorite"] = not memory["favorite"]

        json_name = memory["filename"].replace(
            ".jpg",
            ".json"
        )

        json_path = os.path.join(
            self.memory_folder,
            json_name
        )

        metadata = {

            "filename": memory["filename"],
            "timestamp": memory["timestamp"],
            "description": memory["description"],
            "objects": memory["objects"],
            "tags": memory["tags"],
            "favorite": memory["favorite"]

        }

        with open(json_path, "w") as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

        print(
            f"{memory['filename']} favorite = {memory['favorite']}"
        )

        return True

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def total_memories(self):

        return len(self.frames)

    def total_favorites(self):

        return len(self.get_favorites())

    # -------------------------------------------------
    # Gallery Preview
    # -------------------------------------------------

    def display_gallery(self, frame):

        thumb_w = 140
        thumb_h = 100
        spacing = 10

        max_memories = 5

        memories = self.frames[:max_memories]

        for i, memory in enumerate(memories):

            thumb = cv2.resize(
                memory["image"],
                (thumb_w, thumb_h)
            )

            x = 10 + i * (thumb_w + spacing)
            y = frame.shape[0] - thumb_h - 20

            frame[
                y:y + thumb_h,
                x:x + thumb_w
            ] = thumb

            cv2.rectangle(
                frame,
                (x - 2, y - 2),
                (x + thumb_w + 2,
                 y + thumb_h + 2),
                (0, 255, 255),
                2
            )

            cv2.putText(

                frame,

                memory["timestamp"].split(" ")[1],

                (x + 5,
                 y + thumb_h + 15),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.45,

                (255, 255, 255),

                1

            )

            if memory["favorite"]:

                cv2.putText(

                    frame,

                    "★",

                    (x + thumb_w - 25,
                     y + 20),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.8,

                    (0, 255, 255),

                    2

                )