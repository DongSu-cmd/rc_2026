
import cv2
import threading
from flask import Flask, Response

app = Flask(__name__)

frame = None

def camera_thread():
    global frame

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera Open Fail")
        return

    while True:
        ret, img = cap.read()

        if not ret:
            continue

        frame = img

@app.route("/camera")
def camera():

    global frame

    if frame is None:
        return "No Frame"

    ret, buffer = cv2.imencode(
        ".jpg",
        frame,
        [cv2.IMWRITE_JPEG_QUALITY, 60]
    )

    if not ret:
        return "Encode Error"

    return Response(
        buffer.tobytes(),
        mimetype="image/jpeg"
    )

if __name__ == "__main__":

    t = threading.Thread(
        target=camera_thread,
        daemon=True
    )

    t.start()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
