FROM python:3.8-slim

# Install pip
RUN apt update -y
RUN apt install python3-pip -y

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz
RUN tar xzvf geckodriver-v0.32.0-linux64.tar.gz
RUN rm geckodriver-v0.32.0-linux64.tar.gz


