#!/usr/bin/env python3
# Created at Mar 7, 2018, by Qi Zhang

import sys

from setuptools import setup

PY3 = sys.version_info

if PY3 < (3, 5):
    raise EnvironmentError('Please use CPython interpreter higher than version 3.5!')

__author__ = {'Qi Zhang': 'qz2280@columbia.edu'}
__copyright__ = 'Copyright (c) 2018, Qi Zhang'
__date__ = 'Mar 7, 2018'
__maintainer__ = 'Qi Zhang'

setup(
    name='text_stream',
    version='0.1.0',
    packages=['text_stream', 'text_stream.tests'],
    url='https://github.com/singularitti/text_stream',
    license='MIT',
    author='Qi Zhang',
    author_email='qz2280@columbia.edu',
    description='A package for streaming text data model'
)
