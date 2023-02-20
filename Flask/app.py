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

global models
models = MLModel()
# model = models.select_model("logistic_regression")
model = models.select_model("BertSent")
final_model = model.get_model()

@app.route('/',methods = ['POST', 'GET'])
def index_page():
    # Posting the topic recieved from the Front end to the Backend Kafka database
    if request.method == 'POST':
        topic = request.form.get("topic")
        host = "127.0.0.1"
        port = 8004

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send(topic.encode())

            print(s.recv(1024).decode())

            return redirect(url_for('result'))

    return render_template("index.html")

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
    # Sending the tweets recieved from Kafka Backend to the Front end with sentiments
    consumer = KafkaConsumer("twitter_data",bootstrap_servers="localhost:9092")
    for msg in consumer:
        json_data = json.loads(msg.value.decode("utf-8"))
        text_data = json_data["data"]["text"]
        # Predicting sentiment as Positive, Negative or Neutral
        prediction = get_prediction(text_data)
        print("Prediction: ",prediction)
        text_prediction = {"text":text_data, "pred":prediction}
        # Emitting the predictions and text data to the front-end
        socketio.emit('sending_message',text_prediction)
        socketio.emit('sending_prediction', str(prediction))
        socketio.sleep(1)

def get_prediction(text):
    prediction = model.predict(final_model, [text])
    return prediction

@app.route('/result')
def result():
    return render_template("result.html")

if __name__ == "__main__":
    socketio.run(app, port=5003)