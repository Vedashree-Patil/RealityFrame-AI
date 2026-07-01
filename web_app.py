import cv2
from flask import Flask, render_template, Response, redirect, url_for

from modules.camera_stream import generate_frames
from modules.frame_manager import FrameManager

app = Flask(__name__)

frame_manager = FrameManager()
camera = cv2.VideoCapture(0)


@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        memories=frame_manager.get_frames()
    )


@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/capture", methods=["POST"])
def capture():

    success, frame = camera.read()

    if success:
        frame = cv2.flip(frame, 1)
        frame_manager.capture(frame)

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)

@app.route("/gallery")
def gallery():
    return render_template(
        "gallery.html",
        memories=frame_manager.get_frames()
    )


@app.route("/favorites")
def favorites():
    return render_template(
        "favorites.html",
        memories=frame_manager.get_frames()
    )


@app.route("/search")
def search():
    return render_template(
        "search.html",
        memories=frame_manager.get_frames()
    )


@app.route("/settings")
def settings():
    return "<h2>Settings Coming Soon</h2>"

@app.route("/memory/<int:index>")
def memory(index):

    memories = frame_manager.get_frames()

    if index >= len(memories):
        return "Memory not found"

    return render_template(
        "memory.html",
        memory=memories[index]
    )