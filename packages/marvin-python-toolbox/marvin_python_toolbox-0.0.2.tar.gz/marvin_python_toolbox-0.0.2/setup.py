#!/usr/bin/env python
# coding=utf-8

# Copyright [2017] [B2W Digital]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from setuptools.command.develop import develop as _develop
from setuptools.command.install import install as _install
import shutil

# Package basic info
PACKAGE_NAME = 'marvin_python_toolbox'
PACKAGE_DESCRIPTION = 'Marvin Python Toolbox'

URL = 'https://github.com/marvin-ai/marvin-python-toolbox'

AUTHOR_NAME = 'Daniel Takabayashi'
AUTHOR_EMAIL = 'daniel.takabayashi@gmail.com'

PYTHON_2 = True
PYTHON_3 = False

# Project status
# (should be 'planning', 'pre-alpha', 'alpha', 'beta', 'stable', 'mature' or 'inactive').
STATUS = 'stable'

# Project topic
# See https://pypi.python.org/pypi?%3Aaction=list_classifiers for a list
TOPIC = 'Topic :: Software Development :: Libraries :: Python Modules',

# External dependencies
# More info https://pythonhosted.org/setuptools/setuptools.html#declaring-dependencies
REQUIREMENTS_EXTERNAL = [
    'six>=1.10.0',
    'bumpversion>=0.5.3',
    'click>=3.3',
    'jupyter>=1.0.0',
    'pep8>=1.7.0',
    'virtualenv>=15.0.1',
    'pytest-cov>=1.8.1',
    'mock>=2.0.0',
    'tox==2.2.0',
    'pytest-watch>=4.1.0',
    'pytest-testmon>=0.8.2',
    'jsonschema>=2.5.1',
    'pytest==2.9.2',
    'pytest-flask>=0.10.0',
    'python-slugify==0.1.0',
    'paramiko==2.1.2',
    'PyHive==0.3.0',
    'thrift==0.10.0',
    'thrift-sasl==0.2.1',
    'virtualenvwrapper>=4.7.1'
    'requests==2.5.1',
    'python-dateutil==2.4.2',
    'python-slugify==0.1.0',
    'path.py==7.2',
    'httpretty==0.8.4',
    'jsonschema>=2.5.1',
    'gprof2dot',
    'ujsonpath==0.0.2',
    'simplejson>=3.10.0',
    'configobj>=5.0.6',
    'findspark==1.1.0',
    'grpcio==1.6.0',
    'grpcio-tools==1.6.0',
    'joblib==0.11',
    'autopep8==1.3.3',
    'progressbar2==3.34.3'
]

# Test dependencies
REQUIREMENTS_TESTS = []

# This is normally an empty list
DEPENDENCY_LINKS_EXTERNAL = []

# script to be used
SCRIPTS = ['bin/marvin']


def _get_version():
    """Return the project version from VERSION file."""
    with open(os.path.join(os.path.dirname(__file__), PACKAGE_NAME, 'VERSION'), 'rb') as f:
        version = f.read().decode('ascii').strip()
    return version


def _hooks(dir):
    _set_autocomplete()
    _install_notebook_extension()


def _set_autocomplete():

    virtualenv = os.environ.get('VIRTUAL_ENV', None)

    if virtualenv:
        postactivate = os.path.join(virtualenv, 'bin', 'postactivate')

        if os.path.exists(postactivate):
            shutil.copy(
                os.path.join('marvin_python_toolbox', 'extras', 'marvin_bash_completion'),
                os.path.join(virtualenv, 'marvin_bash_completion')
            )

            command = 'source "{}"'.format(os.path.join(virtualenv, 'marvin_bash_completion'))

            with open(postactivate, 'r+') as fp:
                lines = fp.readlines()
                fp.seek(0)
                configured = False
                for line in lines:
                    if 'marvin_bash_completion' in line:
                        # Replacing old autocomplete configuration
                        fp.write(command)
                        configured = True
                    else:
                        fp.write(line)

                if not configured:
                    fp.write(command)
                    # 'Autocomplete was successfully configured'
                fp.write('\n')
                fp.truncate()


def _install_notebook_extension():
    import marvin_python_toolbox as toolbox

    install_command = [
        "jupyter",
        "nbextension",
        "install",
        os.path.join(toolbox.__path__[0], 'extras', 'notebook_extensions', 'main.js'),
        "--destination",
        "marvin.js",
        "--sys-prefix",
        "--overwrite"
    ]

    os.system(' '.join(install_command))

    enable_command = [
        "jupyter",
        "nbextension",
        "enable",
        "marvin",
        "--sys-prefix"
    ]

    os.system(' '.join(enable_command))


class develop(_develop):
    def run(self):
        _develop.run(self)
        self.execute(_hooks, (self.install_lib,), msg="Running develop preparation task")


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_hooks, (self.install_lib,), msg="Running install preparation task")


class Tox(TestCommand):
    """Run the test cases using TOX command."""
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        else:
            # Run all tests by default
            args = ['-c', os.path.join(os.path.dirname(__file__), 'tox.ini'), 'tests']
        errno = tox.cmdline(args=args)
        sys.exit(errno)


DEVELOPMENT_STATUS = {
    'planning': '1 - Planning',
    'pre-alpha': '2 - Pre-Alpha',
    'alpha': 'Alpha',
    'beta': '4 - Beta',
    'stable': '5 - Production/Stable',
    'mature': '6 - Mature',
    'inactive': '7 - Inactive',
}

CLASSIFIERS = ['Development Status :: {}'.format(DEVELOPMENT_STATUS[STATUS])]
if PYTHON_2:
    CLASSIFIERS += [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ]
if PYTHON_3:
    CLASSIFIERS += [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ]

setup(
    name=PACKAGE_NAME,
    version=_get_version(),
    url=URL,
    description=PACKAGE_DESCRIPTION,
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    author=AUTHOR_NAME,
    maintainer=AUTHOR_NAME,
    maintainer_email=AUTHOR_EMAIL,
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS_EXTERNAL,
    tests_require=REQUIREMENTS_TESTS,
    dependency_links=DEPENDENCY_LINKS_EXTERNAL,
    scripts=SCRIPTS,
    cmdclass={'test': Tox, 'develop': develop, 'install': install},
)