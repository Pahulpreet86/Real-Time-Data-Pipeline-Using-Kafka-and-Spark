import time
import json
import requests
import datetime
from kafka import KafkaProducer, KafkaClient
from websocket import create_connection


def get_sensor_data_stream():
    try:
        url = 'http://0.0.0.0:3030/sensordata'
        r = requests.get(url)
        return r.text
    except:
        return "Error in Connection"


producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

while True:
    msg =  get_sensor_data_stream()
    producer.send("RawSensorData", msg.encode('utf-8'))
    time.sleep(1)


    

