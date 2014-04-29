#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='scarlett',
    version='0.1.0',
    description='S.C.A.R.L.E.T.T is Tony Darks artificially programmed intelligent computer. It is programmed to speak with a female voice in a British accent.',
    long_description=readme + '\n\n' + history,
    author='Malcolm Jones',
    author_email='@bossjones',
    url='https://github.com/bossjones/scarlett',
    packages=[
        'scarlett',
    ],
    package_dir={'scarlett':
                 'scarlett'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='scarlett',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)