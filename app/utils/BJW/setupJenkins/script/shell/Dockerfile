#!Dockerfile
FROM jenkins/jenkins:2.346.3-jdk11

USER root

#
# Install Docker
#

RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli

#
# Jenkins plugins
#

COPY ./plugins.txt /usr/share/jenkins/plugins.txt
RUN jenkins-plugin-cli --plugins -f /usr/share/jenkins/plugins.txt

USER jenkins
ENV JENKINS_USER admin
ENV JENKINS_PASS admin

#
# Skip initial setup
#
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
ENV JAVA_OPTS -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true