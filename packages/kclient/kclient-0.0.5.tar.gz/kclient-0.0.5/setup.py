#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="kclient",
    version="0.0.5",
    url='https://github.com/keyaks/k-client',
    author='keyaks',
    author_email='37239686+keyaks@users.noreply.github.com',
    maintainer='keyaks',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(),
    install_requires= open('requirements.txt').read().splitlines(),
)