import cv2
import numpy as np
import base64
from flask import Flask, Response, request, render_template

app = Flask(__name__)

latest_frame = None  # Store the latest received frame


@app.route('/')
def index():
    return render_template('index.html')  # Serve the mobile streaming page


@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    global latest_frame
    data = request.json['frame']

    # Decode base64 image
    header, encoded = data.split(",", 1)
    image_data = base64.b64decode(encoded)
    np_arr = np.frombuffer(image_data, np.uint8)
    latest_frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return "Frame received", 200


def generate_frames():
    global latest_frame
    while True:
        if latest_frame is not None:
            _, buffer = cv2.imencode('.jpg', latest_frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
