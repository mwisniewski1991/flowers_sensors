# Flowers Sensor

## Goal:
Create dataflow from sensors through database to dashboard.


## Stack:

- Nginx
- Python
    - Flask
- RabbitMQ
- Database - InfluxDB,
- Visualization - Grafana


## Project details:

Sensors will created data.
API will be bridge to communicate with RabbitMQ.
Python app will get data from queues and put in database.
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
- Powering PICO from batteries - IN PROGRESS
- PICO: led informations
- Sensors errors - IN PROGRESS
- API authentication
