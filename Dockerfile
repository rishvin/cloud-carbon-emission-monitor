FROM python:3.10.9-slim

ARG port

RUN apt-get update -y
RUN apt-get install wget -y
RUN apt-get install curl -y
RUN apt-get install python3-pip -y

RUN mkdir -p $HOME
COPY . $HOME

RUN pip install pip --upgrade && pip install -r requirements.txt

ENV PORT=$port
ENV FLASK_APP=src/apps/carbon_emission_app.py

EXPOSE $PORT

ENTRYPOINT ["python", "/run_services.py"]
