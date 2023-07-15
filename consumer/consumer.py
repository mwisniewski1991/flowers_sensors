import pika
import sys
import os
import json
import time
import logging
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

def connect_influx() -> influxdb_client.InfluxDBClient:
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "mwdev"
    url = "http://0.0.0.0:8086"

    return influxdb_client.InfluxDBClient(
            url=url, 
            token=token, 
            org=org)

def callback(ch, method, properties, body):
    logging.info(f'Push InfluxDB: {body}')

    id, name, temperature, humidity = json.loads(body)


    # org = "mwdev"
    # bucket="storage"
    # write_client = connect_influx()

    # write_api = write_client.write_api(write_options=SYNCHRONOUS)
    
    # humidity_data = influxdb_client.Point("garden").tag('flower', name).field('humidity', humidity)
    # temperature_data = influxdb_client.Point("garden").tag('flower', name).field('temperature', temperature)
    
    # write_api.write(bucket=bucket, org=org, record=humidity_data)
    # write_api.write(bucket=bucket, org=org, record=temperature_data)

def main():
    logger = logging.getLogger()

    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format=" [\mwdev/] %(asctime)s %(levelname)s :::: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        )   
    

    logging.info("Waiting")
    time.sleep(20)

    logging.info("Trying to connect.")
    connection_rabbit = pika.BlockingConnection(pika.ConnectionParameters(
        host='rabbitmq', 
        port=5672))
    
    logging.info("Failed to connect to RabbitMQ service. Message wont be sent.")

    channel = connection_rabbit.channel()
    channel.queue_declare(queue='flowers_data')
    channel.basic_consume(queue='flowers_data', on_message_callback=callback)
    
    logging.info('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)