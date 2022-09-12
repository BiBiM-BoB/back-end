FROM jenkins/jenkins:lts

# 플러그인 설치
COPY --chown=jenkins:jenkins jenkins-plugin-list.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt

# jenkins 사용자 자동 생성
COPY jenkins-setup.groovy /usr/share/jenkins/ref/init.groovy.d/

# jenkins docker 설정
USER root
RUN apt-get update && apt-get install -y \
    python3 \
	python3-pip \
	git \

# python 모듈 설치
RUN python3 -m pip install venv

USER jenkins