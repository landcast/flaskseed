#!/bin/sh
export FLASK_APP=./run.py
sudo mysql -h 127.0.0.1  -uroot -plt7116 < ./sql/dbcreate.sql
rm ./migrations -rf
sudo flask db init
sudo flask db migrate
sudo flask db upgrade
sudo mysqldump -h 127.0.0.1  -uroot -plt7116 ustutor > ./sql/tablecreate.sql
