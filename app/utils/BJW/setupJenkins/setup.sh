#!/bin/bash

WHOAMI="$(whoami)"

sudo apt update
sudo apt-get install -y ca-certificates curl software-properties-common \
  apt-transport-https gnupg lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# install docker and jre
sudo apt install -y docker-ce docker-ce-cli
sudo apt-get install -y openjdk-11-jre

sudo groupadd docker
sudo usermod -aG docker `whoami`

sudo docker build -t bibim-jenkins:0.1 .
sudo docker volume create jenkins