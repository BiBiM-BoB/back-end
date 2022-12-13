#!Dockerfile
FROM jenkins/jenkins:lts

USER root

COPY install_docker.sh /install_docker.sh
RUN chmod +x /install_docker.sh
RUN /install_docker.sh

RUN usermod -aG docker jenkins
RUN setfacl -Rm d:g:docker:rwx,g:docker:rwx /var/run/

#
# Jenkins plugins
#

COPY plugins.txt /usr/share/jenkins/plugins.txt
RUN jenkins-plugin-cli --plugins -f /usr/share/jenkins/plugins.txt

RUN chmod 777 -R /usr/share/jenkins/ref/init.groovy.d/

COPY 00-default-user.groovy /usr/share/jenkins/ref/init.groovy.d/


USER jenkins
ENV JENKINS_USER bibim
ENV JENKINS_PASS bibim

ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
ENV JAVA_OPTS -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true
ENV JAVA_OPTS -Dhudson.slaves.WorkspaceList=_