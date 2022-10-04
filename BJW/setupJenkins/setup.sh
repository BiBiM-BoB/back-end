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
sudo apt install -y docker-ce docker-ce-cli containered.io
sudo apt-get install -y openjdk-11-jre

sudo groupadd docker
sudo usermod -aG docker "${WHOAMI}"

sudo wget -P /home/Downloads/ https://get.jenkins.io/war-stable/2.361.1/jenkins.war

java -jar jenkins.war --httpPort=8080 -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true -Djenkins.install.runSetupWizard=false

read -p "RESTART IS RECOMMENDED.. [Y/n]: " YESORNO

if [ "${YESORNO}" == "Y" ] ; then
  sudo init 6
fi