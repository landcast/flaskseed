# flaskseed -- flask template project for e-learning

## Background

This is a sample web project based on flask. The business model is for
e-learning. It reference much from sandman2 project on github. The main
purpose is to depict the correct way to setup python open-source projects.

## Enviroment

Python 3.6 with flask. Recommand to use pyenv and virtualenv to manage python
versions.

Mysql with account root:lt7116 located at localhost:3306.

Redis with no authorization check located at localhost:6379.

Future will add elastic-search for document storing and searching.


## Build Tool

Using pybuilder for project building, this tool inspired much by java maven.

```
$> pip install -r ./requirements.txt
$> pyb clean
$> pyb
```

The ./target folder contains output, and I add a custom task to copy setup.py
from ./target to ./

## Structure

./ustutor main source of web application ustutor (e-learning).

./doc document will be generated by SPHINX.

./scripts *.py which will be run on $> pip setup.py install

./dbrecreate.sh will drop database and recreate it.

./dbmigrate using flask-migrate for database incremental change.

./debug-ustutor.sh will do debug start and tail the log. If log file location
changed in ./config/settings, do remember to change the log file location in
this script also.

./sql sql file generated by above db*.sh.

./unittests for unit test case. Using $> python -m unittest unittests/*.py to
run all.

./integrationtest currently not used.

./.travis.yml CI setting for github travis-ci integration.

./build.py pybuilder tool config, which control the whole build procedure.

./setup.py for ```$> python setup.py install```, generated by pybuilder

./requirements.txt for ```$> pip install -r requirements.txt```, generated by
pigar(```$> pip install pigar && $> pigar```). Because pigar get dependency by
scan *.py file, it can't find pymysql dependency, so 'pymysql' is added mannually
into requirements.txt

./Makefile currently not used.

./tox.ini currently not used.

## Data Model

Manually written for table generation and SQLAlchemy modeling. The common_models
is the fundamental ware for other business domain model to subclass.

## Other Storage

Currently involve redis for cache and flash storage.

## Restful

```./ustutor/resources``` contains endpoint created by flask-restful.

## Restless

Using flask-restless to generate restful endpoint for every model in models.
In ```./ustutor/__init__.py``` setup_api function using reflection method to control
automated api endpoint generation.

## Swagger

Please notice that the swagger api version is openapi-v3.

In ./ustutor/swaggerapis, the ```__init__.py``` created swagger.json data structure
with /auth preset in. Other model level rest-less apis are generated with
code by reflection.

To access swagger api, open http://localhost:5000/swagger in browser.


## Authentication

JWT authentication used here, the code are distributed in ```./ustutor/__init__.py```.
The intercept policy controlled by auth_check_needed function, and jwt handled in
jwt_check function.

## Authorization

Table controlled authorization, using RoleDefinition, RoleAuth to do that.