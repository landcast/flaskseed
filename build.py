#   bkflask
#   Copyright 2018 Tom Li
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
    A simple flask application tested using pyassert and pyfix and
    built with pybuilder.
"""

from pybuilder.core import use_plugin, init, Author, task, depends
import pymysql
import os

use_plugin('filter_resources')

use_plugin('python.core')
use_plugin('python.coverage')
use_plugin('python.unittest')
use_plugin('python.integrationtest')
use_plugin('python.install_dependencies')
use_plugin('python.flake8')
use_plugin('python.pydev')
use_plugin("python.distutils")

name = 'flaskseed'
authors = [Author('Tom Li', 'landcast@163.com'),
           Author('lxf', 'xxx@xxx.com')]
license = 'Apache License, Version 2.0'
summary = 'Flask template application'
url = 'https://github.com/landcast/flaskseed'
version = '0.1'

default_task = ['install_dependencies', 'analyze', 'publish', 'post_publish']


@task
@depends('publish')
def post_publish(project, logger):
    logger.info('run post_publish task')
    os.system('rm setup.py -rf')
    os.system('cp ./target/dist/flaskseed-0.1/setup.py setup.py')


@init
def set_properties(project):

    project.build_depends_on('coverage')
    project.build_depends_on('pyassert')

    project.depends_on('flask')
    project.depends_on('flask-restful')
    project.depends_on('flask-debugtoolbar')
    project.depends_on('flask-restless')
    project.depends_on('flask-sqlalchemy')
    project.depends_on('flask-redis')
    project.depends_on('flask-cors')
    project.depends_on('flask-migrate')
    project.depends_on('flask-mail')
    project.depends_on('PyJWT')
    project.depends_on('pymysql')
    project.depends_on('elasticsearch')
    project.depends_on('requests')
    project.depends_on('urllib3')
    project.depends_on('python-consul')

    project.set_property('flake8_break_build', False)
    project.set_property("coverage_break_build", False)
    project.set_property_if_unset("pytest_coverage_break_build_threshold", 30)

    project.set_property('dir_source_main_python', 'src')
    project.set_property('dir_source_unittest_python', 'unittests')
    project.set_property('dir_source_main_scripts', 'scripts')
    project.set_property(
        'dir_source_integrationtest_python', 'integrationtests')

    project.set_property('integrationtest_parallel', False)