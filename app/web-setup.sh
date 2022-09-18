#!/bin/bash

# AWS Ubuntu에서 실행된다고 가정(실행시 sudu 필수)
apt-get update
apt install -y mysql-server
apt install -y libmysqlclient-dev

# mysql 실행
systemctl mysql start

# DataBase 생성
mysql -u root -e "CREATE DATABASE devsecopsdb"

# mysql 유저 생성
mysql -u root -e "CREATE USER 'bibimbob'@'%' identified BY '1q2w3e4r!'"
mysql -u root -e "GRANT ALL PRIVILEGES ON devsecopsdb.* TO bibimbob@'%'"

# python 모듈 설치
python3 -m pip install -r requirements.txt

echo "[DONE] web-setup"