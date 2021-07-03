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

echo "Dockerコンテナを作成します。"
docker-compose build
docker-compose up -d

sleep 10
docker exec -it php /bin/sh -c 'composer create-project --prefer-dist laravel/laravel /var/www/html/api'

echo "Laravelで動作するAPIアプリケーションのリンクをNGINXにリンクさせます。"
ln -s ../api/public/ ./web/public/api

echo "DB初期データを取得します。"
docker exec -it python3 /bin/sh -c '/bin/bash /root/opt/setup.sh'


