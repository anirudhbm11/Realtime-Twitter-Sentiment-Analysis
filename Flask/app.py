from flask import Flask, render_template, request, Response, redirect, url_for, stream_template
import socket
from kafka import KafkaConsumer
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

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
        # return render_template("result.html")

    return render_template("index.html")

def stream_template(template_name, **context):                                                                                                                                                 
    app.update_template_context(context)                                                                                                                                                       
    t = app.jinja_env.get_template(template_name)                                                                                                                                              
    rv = t.stream(context)                                                                                                                                                                     
    rv.disable_buffering()                                                                                                                                                                     
    return rv

@socketio.on('json')
def sending_message(json):
    consumer = KafkaConsumer("twitter_data",bootstrap_servers="localhost:9092")
    for msg in consumer:
        send(msg, json=True)

# @app.route('/result')
# def result():
#     consumer = KafkaConsumer("twitter_data",bootstrap_servers="localhost:9092")

#     def sending_message():
#         for msg in consumer:
#             print(msg)
#             yield(str(msg))
    
#     # return Response(sending_message(), mimetype="text/plain")
#     # return Response(sending_message(), mimetype="multipart/x-mixed-replace")
#     rows = sending_message()                                                                                                                                                                          
#     return Response(stream_template('result.html', rows=rows))


if __name__ == "__main__":
    # app.run(port= 5003, debug=True)
    socketio.run(app, port=5003, debug=True)