from flask import Flask, request, jsonify
import json
import pika

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, From Docker.</p>"

@app.route("/sensor", methods=['GET', 'POST'])
def sensor():
    records = request.args
    message = json.dumps(records)

    try:    
        connection_rabbit = pika.BlockingConnection(pika.ConnectionParameters(
            host='rabbitmq', 
            port=5672))
        
    except pika.exceptions.AMQPConnectionError:
        return "Failed to connect to RabbitMQ service. Message wont be sent."

    channel = connection_rabbit.channel()
    channel.queue_declare(queue='flowers_data')

    channel.basic_publish(
        exchange='',
        routing_key='flowers_data',
        body=message                        
    ) 

    return records


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')