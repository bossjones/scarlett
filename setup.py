#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys

from scarlett import __version__ as version

try:
    #from setuptools import setup, find_packages
    from setuptools import setup
    # might need this later
    extra = dict(test_suite="tests.test.suite", include_package_data=True)
except ImportError:
    from distutils.core import setup
    extra = {}

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")

static = {}

for root, dirs, files in os.walk('static'):
    for filename in files:
        filepath = os.path.join(root, filename)

        if root not in static:
            static[root] = []

        static[root].append(filepath)

# Might use this later
try:
    here = os.path.abspath(os.path.dirname(__file__))
except:
    pass


def read_requirements(filename):
    content = open(os.path.join(here, filename)).read()
    requirements = map(lambda r: r.strip(), content.splitlines())
    return requirements


requirements = read_requirements('requirements.txt')
test_requirements = read_requirements('requirements_dev.txt')

# Build manpages if we're making a source distribution tarball.
# if 'sdist' in sys.argv:
# Go into the docs directory and build the manpage.
###     docdir = os.path.join(os.path.dirname(__file__), 'docs')
###     curdir = os.getcwd()
# os.chdir(docdir)
# try:
###         subprocess.check_call(['make', 'man'])
# finally:
# os.chdir(curdir)
###
# Copy resulting manpages.
###     mandir = os.path.join(os.path.dirname(__file__), 'man')
# if os.path.exists(mandir):
# shutil.rmtree(mandir)
###     shutil.copytree(os.path.join(docdir, '_build', 'man'), mandir)

setup(
    name="scarlett",
    version=version,
    description="S.C.A.R.L.E.T.T is Tony Darks artificially programmed intelligent computer. It is programmed to speak with a female voice in a British accent.",
    long_description=readme + "\n\n" + history,
    author="Malcolm Jones",
    author_email="@bossjones",
    url="https://github.com/bossjones/scarlett/",
    packages=[
        "scarlett",
        "scarlett.basics",
        "scarlett.core",
        "scarlett.features",
        "scarlett.brain",
        #"scarlett.features.time",
        "scarlett.listener"

    ],
    package_dir={"scarlett":
                 "scarlett"},
    data_files=static.items(),
    install_requires=[
    ],
    scripts=[
        'bin/scarlett',
        'bin/scarlett_daemon',
        'bin/scarlett_echo_client_test.py',
        'bin/scarlett_worker_cb_test.py',
        'bin/catwav',
        'bin/silence',
        'bin/resample_for_ps',
        'bin/pad_wav'],
    license="BSD",
    platforms="Posix; MacOS X",
    zip_safe=False,
    keywords="scarlett",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
    ],
    **extra
)
