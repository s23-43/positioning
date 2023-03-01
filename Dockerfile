FROM ubuntu:20.04
ENV PYTHONUNBUFFERED=1
WORKDIR /app/
COPY . .

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y python3 python3-pip
RUN pip install --upgrade pip
RUN pip install scipy