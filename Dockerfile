FROM python:3.7-slim as build

RUN mkdir -p /app/beondietapp/

COPY . /app/beondietapp/

WORKDIR /app/

RUN apt-get update && apt-get install -y cmake bison flex

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt /tmp

WORKDIR /tmp

RUN pip install -r requirements.txt

WORKDIR /app/beondietapp/


CMD ["python", "run.py"]
