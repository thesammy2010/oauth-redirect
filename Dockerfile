FROM python:3.9.0-slim-buster

WORKDIR /home
COPY . /home

RUN pip install -r requirements.txt --quiet

EXPOSE 8080

ENV FLASK_ENV production


# start server
ENTRYPOINT python run.py