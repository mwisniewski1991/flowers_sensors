from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import pika
import logging
import sys


KAFKA_FLOWERS_TOPIC = "flowers_data"

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="[\mwdev/] %(asctime)s %(levelname)s :::: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    )   

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, From Docker.</p>"

@app.route("/sensor", methods=['GET', 'POST'])
def sensor():

    logging.info("STARTING")
    
    flowers_data = request.args
    producer = KafkaProducer(bootstrap_servers='kafka:29092', value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    producer.send(
        KAFKA_FLOWERS_TOPIC,
        flowers_data
    )

    return flowers_data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')