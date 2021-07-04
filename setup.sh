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
mkdir web
mkdir web/public

echo "Redisコンテナ用にディレクトリを作成します"
echo "Create redis Directory"
mkdir redis

echo "REST API用にディレクトリを作成します。"
mkdir restapi

echo "Dockerコンテナを作成します。"
docker-compose build
docker-compose up -d

echo "Docker起動遅延30秒"
sleep 30

echo "DB初期データを取得します。"
docker exec -it python3 /bin/sh -c '/bin/bash /root/opt/setup.sh'

docker exec -it -d restapi /bin/bash -c 'uvicorn main:app --reload --host 0.0.0.0 --port 80'
