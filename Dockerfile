FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

RUN apt-get update
RUN apt-get install net-tools -y
RUN apt-get install apache2 -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
COPY ./app/requirements.txt /home
COPY ./docker-web-setup.sh /home
RUN ["chmod", "+x", "/home/docker-web-setup.sh"]
RUN /home/docker-web-setup.sh
RUN pip3 install cryptography
RUN pip3 install -r /home/requirements.txt
RUN apt-get install git -y
RUN service mysql start
COPY app /home/app
WORKDIR /home
EXPOSE 52211