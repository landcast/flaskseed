#!/bin/sh
export EXTERNALCFG=../config/settings-prd.py
export FLASK_APP=./run.py
sudo mysql -h rm-2ze6kzf5ig80613f7vo.mysql.rds.aliyuncs.com  -uustutor -pUs_Tutor < ./sql/dbcreate.sql
rm ./migrations -rf
flask db init
flask db migrate
flask db upgrade
sudo mysqldump -h rm-2ze6kzf5ig80613f7vo.mysql.rds.aliyuncs.com  -uustutor -pUs_Tutor  ustutor > ./sql/tablecreate.sql
