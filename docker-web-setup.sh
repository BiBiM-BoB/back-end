#!/bin/bash

# ubuntu docker에서 실행된다고 가정(실행시 sudu 필수)
apt-get update

# mysql 설치
apt-get install -y mysql-server
apt-get install -y libmysqlclient-dev
apt-get install -y wget

# mysql 실행
service mysql start

# DataBase 생성
mysql -u root -e "CREATE DATABASE devsecopsdb"

# mysql 유저 생성
mysql -u root -e "CREATE USER 'bibimbob'@'%' identified BY '1q2w3e4r!'"
mysql -u root -e "GRANT ALL PRIVILEGES ON devsecopsdb.* TO bibimbob@'%'"

echo "[DONE] web-setup"