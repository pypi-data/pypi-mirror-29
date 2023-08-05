#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @namespace requests-mv-integrations
#
#    Copyright (c) 2018 TUNE, Inc.
#    All rights reserved.
#

from __future__ import with_statement

# To install the tune-mv-integration-python library, open a Terminal shell,
# then run this file by typing:
#
# python setup.py install
#

import sys
import re
import codecs

from setuptools import setup

REQUIREMENTS = [
    req for req in open('requirements.txt')
    .read().split('\n')
    if req != ''
]

PACKAGES = [
    'requests_mv_integrations',
    'requests_mv_integrations.errors',
    'requests_mv_integrations.exceptions',
    'requests_mv_integrations.support',
    'requests_mv_integrations.support.response'
]

TEST_REQUIREMENTS = ['pytest>=3.2.5', 'pytest-cov']

with open('requests_mv_integrations/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

if len(sys.argv) < 2 or sys.argv[1] == 'version':
    print(version)
    sys.exit()

CLASSIFIERS = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: PyPy'
]

with codecs.open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with codecs.open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='requests-mv-integrations',
    version=version,
    description="Extension of Python HTTP `requests` with verbose logging using `logging-mv-integrations`.",
    long_description=readme + '\n\n' + history,
    author='TUNE Inc.',
    author_email='jefft@tune.com',
    url='https://github.com/TuneLab/requests-mv-integrations',
    download_url='https://github.com/TuneLab/requests-mv-integrations/archive/v{0}.tar.gz'.format(version),
    keywords="requests tune multiverse",
    license='MIT License',
    zip_safe=False,
    include_package_data=True,
    install_requires=REQUIREMENTS,
    packages=PACKAGES,
    package_data={'': ['LICENSE']},
    package_dir={'requests-mv-integrations': 'requests-mv-integrations'},
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=TEST_REQUIREMENTS,
    classifiers=CLASSIFIERS
)
