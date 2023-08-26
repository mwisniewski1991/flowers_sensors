# Flowers Sensor

## Goal:
Create dataflow from sensors through database to dashboard.


## Stack:

- Nginx
- Python
    - Flask
- Kafka
- Database 
    - InfluxDB,
- Visualization 
    - Grafana


## Project details:

Sensors will created data.
API will be bridge to communicate with Kafka.
Python app will get data from Kafka and put in database.
From data in database dashboard will create charts.

### Services
- API - Python Flask
- Message queue - RabbitMQ
- Message consumer - Python
- Database - InfluxDB
- Visualization - Grafana

## To Do Plan
- Create Consumer - DONE
- Create InfluxDB Container - DONE
- Connect consumeer with InfluxDB - DONE
- Create Grafana conteiner - DONE
- Connect Grafana to Influxdb - DONE
- Change from RabbitMQ to Kafka - DONE
- Powering PICO from batteries - IN PROGRESS
- Sensors errors - IN PROGRESS
- PICO: led informations
- API authentication