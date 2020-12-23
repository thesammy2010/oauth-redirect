FROM python:3.9.1-slim-buster

WORKDIR /home
COPY . /home

RUN pip install -r requirements.txt

# start server
ENTRYPOINT python run.py