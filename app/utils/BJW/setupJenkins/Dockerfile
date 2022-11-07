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

RUN /usr/local/bin/install-plugins.sh \
  windows-slaves \
  matrix-auth \
  matrix-project \
  antisamy-markup-formatter \
  script-security \
  pipeline-model-declarative-agent \
  pipeline-stage-step \
  pipeline-input-step \
  slack \
  git \
  blueocean

COPY ref /usr/share/jenkins/ref

USER jenkins
ENV JENKINS_USER admin
ENV JENKINS_PASS admin

#
# Skip initial setup
#
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
ENV JAVA_OPTS -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true