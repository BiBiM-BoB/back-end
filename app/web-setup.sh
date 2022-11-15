#!/bin/bash

# AWS Ubuntu에서 실행된다고 가정(실행시 sudu 필수)
apt-get update

# mysql 설치
apt install -y mysql-server
apt install -y libmysqlclient-dev

# mysql 실행
systemctl mysql start

# DataBase 생성
mysql -u root -e "CREATE DATABASE devsecopsdb"

# mysql 유저 생성
mysql -u root -e "CREATE USER 'bibimbob'@'%' identified BY '1q2w3e4r!'"
mysql -u root -e "GRANT ALL PRIVILEGES ON devsecopsdb.* TO bibimbob@'%'"

# mongodb 설치 과정
# https://www.cloudbooklet.com/how-to-install-mongodb-on-ubuntu-22-04/
sudo apt install gnupg
# libssl1 의존성 해결
echo "deb http://security.ubuntu.com/ubuntu impish-security main" | sudo tee /etc/apt/sources.list.d/impish-security.list
sudo apt update
sudo apt install libssl1.1
# mongodb 공개키 다운로드
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
# mongodb repo 설정
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
# mongodb 설치
sudo apt update
sudo apt install -y mongodb-org
# mongodb system setting
sudo systemctl enable mongod
sudo service mongod start

# mongodb collection 생성
mongo --eval ""

# python 모듈 설치
python3 -m pip install -r requirements.txt

echo "[DONE] web-setup"