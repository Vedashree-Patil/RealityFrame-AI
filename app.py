import cv2

from flask import (
    Flask,
    render_template,
    Response,
    redirect,
    url_for,
    send_from_directory,
    request
)

from modules.camera_stream import generate_frames
from modules.frame_manager import FrameManager

app = Flask(__name__)

# -------------------------------
# Initialize Frame Manager & Camera
# -------------------------------

frame_manager = FrameManager()
camera = cv2.VideoCapture(0)


# -------------------------------
# Dashboard
# -------------------------------

@app.route("/")
def dashboard():

    memories = frame_manager.get_frames()

    return render_template(
        "dashboard.html",
        memories=memories
    )


# -------------------------------
# Live Camera Feed
# -------------------------------

@app.route("/video")
def video():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# -------------------------------
# Capture Memory
# -------------------------------

@app.route("/capture", methods=["POST"])
def capture():

    success, frame = camera.read()

    if success:

        frame = cv2.flip(frame, 1)

        frame_manager.capture(frame)

    return redirect(url_for("dashboard"))


# -------------------------------
# Gallery
# -------------------------------

@app.route("/gallery")
def gallery():

    return render_template(
        "gallery.html",
        memories=frame_manager.get_frames()
    )


# -------------------------------
# Favorites
# -------------------------------

@app.route("/favorites")
def favorites():

    return render_template(
        "favorites.html",
        memories=frame_manager.get_frames()
    )


# -------------------------------
# Search
# -------------------------------

@app.route("/search")
def search():

    query = request.args.get("query", "").lower()

    memories = frame_manager.get_frames()

    if query == "":

        filtered = memories

    else:

        filtered = []

        for memory in memories:

            filename = memory.get("filename", "").lower()
            description = memory.get("description", "").lower()

            tags = " ".join(memory.get("tags", [])).lower()

            objects = " ".join(memory.get("objects", [])).lower()

            if (
                query in filename
                or query in description
                or query in tags
                or query in objects
            ):
                filtered.append(memory)

    return render_template(
        "search.html",
        memories=filtered
    )


# -------------------------------
# Individual Memory Page
# -------------------------------

@app.route("/memory/<int:index>")
def memory(index):

    memories = frame_manager.get_frames()

    if index < 0 or index >= len(memories):

        return "Memory Not Found"

    return render_template(
        "memory.html",
        memory=memories[index]
    )


# -------------------------------
# Serve Saved Images
# -------------------------------

@app.route("/frames/<filename>")
def frame(filename):

    return send_from_directory(
        "frames",
        filename
    )


# -------------------------------
# Toggle Favourite
# -------------------------------

@app.route("/favorite/<int:index>")
def favorite(index):

    frame_manager.toggle_favourite(index)

    return redirect(request.referrer or url_for("gallery"))


# -------------------------------
# Delete Memory
# -------------------------------

@app.route("/delete/<int:index>")
def delete(index):

    frame_manager.delete_memory(index)

    return redirect(url_for("gallery"))


# -------------------------------
# Settings
# -------------------------------

@app.route("/settings")
def settings():

    return render_template("settings.html")


# -------------------------------
# Run Application
# -------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )