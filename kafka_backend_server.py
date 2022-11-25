import socket
from kafka import KafkaProducer
import time
from twitter_streaming.twitter_api import TwitterStreamAPI
import json

hostname = "127.0.0.1"
port = 8002

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((hostname,port))
    s.listen()
    
    while True:
        conn, addr = s.accept()

        with conn:
            print("Connection accepted from " + str(addr))
            
            data = conn.recv(1024).decode()
            print("Recieved data: " + str(data))
            if not data:
                print("No topic sent from frontend")
                break

            producer = KafkaProducer(bootstrap_servers= "localhost:9092",linger_ms=5000)

            twitter_stream = TwitterStreamAPI()

            topics = [
                        {"value": "#ftx"},
                        # {"value": "cat has:images -grumpy", "tag": "cat pictures"},
                    ]

            stream = twitter_stream.get_stream(topics)

            for tweet in stream.iter_lines():
                json_response = json.loads(tweet)
                print(json.dumps(json_response, indent=4, sort_keys=True))
                producer.send("twitter_data", tweet)
                producer.flush()
                time.sleep(1)



