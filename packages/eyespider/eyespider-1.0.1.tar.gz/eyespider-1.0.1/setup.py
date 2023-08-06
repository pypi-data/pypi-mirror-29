#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='eyespider',
    version='1.0.1',
    author='Chuck Huang',
    description="A simple,qiuck scraping micro-framework",
    author_email='chuckhunagcm@gmail.com',
    install_requires=['lxml', 'requests', 'cchardet', 'cssselect'],
    url="https://github.com/BlueRagdoll/eyespider/blob/master/README.md",
    packages=find_packages(),
    package_data={'eyespider': ['utils/*.txt']})
