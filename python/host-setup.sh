#!/bin/bash

# AWS Ubuntu에서 실행된다고 가정(실행시 sudu 필수)
apt-get update
apt install -y docker.io 
apt-get install -y docker-compose
apt install -y default-jre

# docker 그룹에 유저 추가
usermod -aG docker ubuntu

systemctl restart docker

# 재부팅 자동 설정
systemctl enable docker

# jenkins 기본 사용자 계정 패스워드 설정
export JENKINS_PW=$(openssl rand -base64 16)
export JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

# docker compose build
docker-compose up -d --build

# jenkins-setup.groovy 대기
sleep 45

# 파이프라인 생성을 위한 jenkins-cli 다운로드
env -i /bin/bash -c 'wget http://127.0.0.1:8080/jnlpJars/jenkins-cli.jar'

sleep 5
# jenkins pipeline 생성
java -jar ./jenkins-cli.jar -s http://localhost:8080 -auth test:$JENKINS_PW create-job pythonpipeline < config.xml

echo "[DONE] host setup!!"