FROM python:3.10.9-slim
ARG port

RUN apt-get update -y
RUN apt-get install wget -y
RUN apt-get -y install curl -y
RUN apt-get install libgomp1 -y
RUN apt-get install software-properties-common curl gnupg2 apt-transport-https -y
RUN wget -O- https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc | apt-key add -
RUN echo "deb https://packages.erlang-solutions.com/ubuntu focal contrib" | tee /etc/apt/sources.list.d/erlang.list
RUN apt-get install erlang -y

RUN curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.deb.sh | bash
RUN apt-get update -y
RUN apt-get install rabbitmq-server -y

RUN mkdir -p $HOME
COPY . $HOME

RUN pip install pip --upgrade && pip install -r requirements.txt

ENV PORT=$port
ENV FLASK_APP=src/apps/carbon_emission_app.py

EXPOSE $PORT

ENTRYPOINT ["sh", "-c", "/docker_run"]
