#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
from distutils.core import setup
from bwg.bwg_api import BWG

setup(
    name='bwg-api',
    version='0.1.0',
    description='BWG API',
    long_description=BWG.__doc__,
    author='flytrap',
    author_email='hiddenstat@gmail.com',
    url='https://github.com/flytrap/bwg-api',
    packages=['bwg'],
    install_requires=[
        "requests==2.19.1",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
