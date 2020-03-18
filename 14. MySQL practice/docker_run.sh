#! /bin/bash
docker run --name mysql57 -p 3306:3306 --rm -de MYSQL_ROOT_PASSWORD=passw mysql:5.7
echo "Waiting for MySQL start"
sleep 15
docker exec -i mysql57 mysql -uroot -ppassw < sales.sql
docker exec -it mysql57 mysql -uroot -ppassw test

