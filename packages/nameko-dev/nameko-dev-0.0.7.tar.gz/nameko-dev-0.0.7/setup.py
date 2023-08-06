#!/usr/bin/env python
import os

from setuptools import find_packages, setup

setup(
    name='nameko-dev',
    version='0.0.7',
    description='A extension of nameko with the run command having autoreloading',
    author='jdahlkar',
    url='http://github.com/dahlkar/nameko-dev',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        "nameko>=2.6.0"
    ],
    entry_points={
        'console_scripts': [
            'nameko-dev=nameko_dev.main:main',
        ],
    },
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
