FROM ubuntu
RUN apt update
RUN apt install -y python3.6 python3-pip ruby ruby-dev rubygems build-essential
RUN gem install --no-document fpm

RUN mkdir /glacier
WORKDIR /glacier

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src/ src/
RUN fbs freeze
RUN fbs installer