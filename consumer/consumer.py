import pika
import sys
import os
import json
import time
import logging
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

def parse_flower_apidata(object: dict) -> list[str]:
    data = json.loads(object)
    flower_id, flower_name, temperature, soil_moisture, humidity = data.values()
    return [flower_id, flower_name, temperature, soil_moisture, humidity]

def connect_influx() -> influxdb_client.InfluxDBClient:
    token = os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
    org = os.environ.get("DOCKER_INFLUXDB_INIT_ORG")
    url = "http://influxdb:8086"

    return influxdb_client.InfluxDBClient(
            url=url, 
            token=token,
            org=org)

def create_flower_points(
        measurement:str, 
        id:str, 
        name:str, 
        temperature:str,
        soil_moisture:str,
        humidity:str
        ) -> list[influxdb_client.Point]:

    temperature_point = influxdb_client.Point(measurement).tag('flower_name', name).tag('flower_id', id).field('temperature', float(temperature))
    soil_moisture_point = influxdb_client.Point(measurement).tag('flower_name', name).tag('flower_id', id).field('soil_mositure', float(soil_moisture))
    humidity_point = influxdb_client.Point(measurement).tag('flower_name', name).tag('flower_id', id).field('humidity', float(humidity))

    return [temperature_point, soil_moisture_point, humidity_point]

def callback(ch, method, properties, body):
    logging.info(f'Push InfluxDB: {body}')

    flower_id, flower_name, temperature, soil_moisture, humidity = parse_flower_apidata(body)

    org = os.environ.get("DOCKER_INFLUXDB_INIT_ORG")
    bucket=os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET")
    
    measurement=os.environ.get("DOCKER_INFLUXDB_MEASUERMENT")

    write_client = connect_influx()
    write_api = write_client.write_api(write_options=SYNCHRONOUS)

    flower_points = create_flower_points(measurement, flower_id, flower_name,  temperature, soil_moisture, humidity)

    for point in flower_points:
        write_api.write(bucket=bucket, org=org, record=point)



def main():
    logger = logging.getLogger()
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="[\mwdev/] %(asctime)s %(levelname)s :::: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        )   
    
    logging.info("Waiting")
    time.sleep(10)

    try:
        logging.info("Trying to connect.")
        connection_rabbit = pika.BlockingConnection(pika.ConnectionParameters(
            host='rabbitmq', 
            port=5672))
        
    except pika.exceptions.AMQPConnectionError:
        logging.info("Failed to connect to RabbitMQ service. Message wont be sent.")
        return None

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