FROM python:3.10-alpine AS builder

WORKDIR /app
COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "consumer.py"]