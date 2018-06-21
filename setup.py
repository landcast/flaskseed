#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'flaskseed',
        version = '0.1',
        description = 'Flask template application',
        long_description = '',
        author = 'Tom Li, lxf',
        author_email = 'landcast@163.com, xxx@xxx.com',
        license = 'Apache License, Version 2.0',
        url = 'https://github.com/landcast/flaskseed',
        scripts = ['scripts/script_run_on_pip_install.py'],
        packages = [
            'models',
            'resources',
            'services',
            'swaggerapis',
            'blueprints.auth',
            'blueprints.live',
            'blueprints.order',
            'blueprints.school',
            'blueprints.student',
            'blueprints.teacher',
            'blueprints.upload'
        ],
        namespace_packages = [],
        py_modules = [
            'dbmigrate',
            'utils',
            '__init__'
        ],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'PyJWT',
            'elasticsearch',
            'flask',
            'flask-cors',
            'flask-debugtoolbar',
            'flask-mail',
            'flask-migrate',
            'flask-redis',
            'flask-restful',
            'flask-restless',
            'flask-sqlalchemy',
            'pymysql',
            'python-consul',
            'requests',
            'urllib3'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
