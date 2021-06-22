#!/bin/sh

echo "Initial Setup"

echo "MySQL(MariaDB)コンテナ用にディレクトリを作成します"
echo "Create MySql Directory"
mkdir mysql
mkdir mysql/data
mkdir mysql/my.cnf
mkdir mysql/initdb.d

echo "Pythonコンテナ用にディレクトリを作成します"
echo "Create Python Directory"
mkdir python

echo "NGINXコンテナ用にディレクトリを作成します"
echo "Create nginx Directory"
mkdir html

echo "Redisコンテナ用にディレクトリを作成します"
echo "Create redis Directory"
mkdir redis

echo "Dockerコンテナを作成します。"
docker-compose build
docker-compose up -d

echo "DB初期データを取得します。"
docker exec -it python3 /bin/sh -c '/bin/bash /root/opt/setup.sh'


