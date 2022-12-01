from flask import Flask, render_template, request, redirect, url_for
import socket
from flask_socketio import SocketIO
from threading import Lock
from kafka import KafkaConsumer
import json
from training.inference import MLModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins='*')

thread = None
thread_lock = Lock()

@app.route('/',methods = ['POST', 'GET'])
def index_page():
    if request.method == 'POST':
        topic = request.form.get("topic")
        host = "127.0.0.1"
        port = 8002

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send(topic.encode())

        return redirect(url_for('result'))

    return render_template("index.html")

# def background_thread():
#     print("Generating random sensor values")
#     while True:
#         dummy_sensor_value = round(random() * 100, 3)
#         socketio.emit('sending_message', {'value': dummy_sensor_value, "date": "today"})
#         # socketio.sleep(1)

@socketio.on('connect')
def connect():
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(sending_message)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

def sending_message():
    consumer = KafkaConsumer("twitter_data",bootstrap_servers="localhost:9092")
    for msg in consumer:
        json_data = json.loads(msg.value.decode("utf-8"))
        text_data = json_data["data"]["text"]
        prediction = get_prediction(text_data)
        print("Prediction: ",prediction)
        socketio.emit('sending_message',text_data)
        socketio.emit('sending_prediction', {"data": str(prediction)})
        socketio.sleep(0)

def get_prediction(text):
    models = MLModel()
    model = models.select_model("logistic_regression")
    prediction = model.predict(["Let's test this out. Not sure how it is gonna work"])[0]
    return prediction

@app.route('/result')
def result():
    return render_template("result.html")


if __name__ == "__main__":
    socketio.run(app, port=5003)