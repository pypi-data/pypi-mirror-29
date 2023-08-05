#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from setuptools import find_packages, setup

requirements = [line.strip() for line in open('requirements.txt', 'r').readlines()]
version      = '0.2.25'

if os.path.isfile('VERSION'):
    version = open('VERSION', 'r').readline().strip() or version

setup(
    name                = 'sonicprobe',
    version             = version,
    description         = 'sonicprobe',
    author              = 'Adrien Delle Cave',
    author_email        = 'pypi@doowan.net',
    license             = 'License GPL-2',
    packages		= find_packages(),
    install_requires    = requirements,
    url                 = 'https://github.com/decryptus/sonicprobe',
    python_requires     = '<3',
)
