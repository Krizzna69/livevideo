import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS for all origins

# Serve the index page
@app.route('/')
def index():
    return render_template('index.html')  # The main HTML page for the viewer

# Handle the signaling messages from the client
@socketio.on('offer')
def handle_offer(data):
    emit('offer', data, broadcast=True)

@socketio.on('answer')
def handle_answer(data):
    emit('answer', data, broadcast=True)

@socketio.on('candidate')
def handle_candidate(data):
    emit('candidate', data, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
