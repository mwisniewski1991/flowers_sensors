# Flowers Sensor

## Goal:
Create dataflow from sensors through database to dashboard.


## Stack:

- Nginx
- Python
    - Flask
- RabbitMQ
- Database - InfluxDB,
- Visualization - Streamlit/Grafana


## Project details:

Sensors will created data.
API will be bridge to communicate with RabbitMQ.
Python app will get data from queues and put in database.
From data in database dashboard will create charts.

## To Do Plan
- Create Consumer
- Create InfluxDB Container
- Connect consumeer with InfluxDB