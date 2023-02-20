import socket
from kafka import KafkaProducer
import time
from twitter_streaming.twitter_api import TwitterStreamAPI
import json

hostname = "127.0.0.1"
port = 8004

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    # Backend Server is listening for topic from front end
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
                        {"value": "{} lang:en".format(data)},
                    ]

            # Getting tweets from Kafka stream
            stream = twitter_stream.get_stream(topics)

            sent = 0

            # Sending tweets to Front-end client
            for tweet in stream.iter_lines():
                try:
                    json_response = json.loads(tweet)
                    print(json.dumps(json_response, indent=4, sort_keys=True))
                    producer.send("twitter_data", tweet)
                    producer.flush()
                    time.sleep(0.5)
                    if sent == 0:
                        msg = "Kafka Sending. Redirecting..."
                        print(msg)
                        conn.send(msg.encode())
                        sent = 1
                except ValueError:
                    continue



