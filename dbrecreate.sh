#!/bin/sh
export FLASK_APP=./run.py
mysql -h 127.0.0.1  -uroot -plt7116 < ./sql/dbcreate.sql
rm ./migrations -rf
flask db init
flask db migrate
flask db upgrade
mysqldump -h 127.0.0.1  -uroot -plt7116 ustutor > ./sql/tablecreate.sql