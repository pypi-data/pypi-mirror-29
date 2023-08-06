#!/usr/bin/env python
from setuptools import setup

setup(
    name="test_kclient",
    version="0.0.1",
    url='https://github.com/keyaks/k-client',
    author='keyaks',
    author_email='37239686+keyaks@users.noreply.github.com',
    maintainer='keyaks',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    install_requires= open('requirements.txt').read().splitlines(),
)