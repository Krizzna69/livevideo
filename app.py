import cv2
import numpy as np
import base64
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets

latest_frame = None  # Store latest frame


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('frame')
def handle_frame(data):
    """Receives a frame from the client (mobile), decodes it, and stores it."""
    global latest_frame
    header, encoded = data.split(",", 1)
    image_data = base64.b64decode(encoded)
    np_arr = np.frombuffer(image_data, np.uint8)
    latest_frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


@socketio.on('request_video')
def stream_video():
    """Continuously sends frames to the client (laptop) using WebSockets."""
    global latest_frame
    while True:
        if latest_frame is not None:
            _, buffer = cv2.imencode('.jpg', latest_frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')
            emit('video_frame', {'frame': frame_data}, broadcast=True)
        socketio.sleep(0.03)  # Adjust to control FPS (~30 FPS)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
