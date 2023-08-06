#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='flask-bootnav',
      version='0.7.0',
      description='Easily create navigation for Flask applications.',
      long_description=read('README.rst'),
      # author='Marc Brinkmann',
      # author_email='git@marcbrinkmann.de',
      # url='http://github.com/mbr/flask-nav',
      license='MIT',
      packages=find_packages(exclude=['tests', 'example']),
      install_requires=['flask', 'visitor', 'dominate'],
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ])
