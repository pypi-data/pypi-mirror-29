#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

from setuptools import setup, find_packages

setup(name='evla_mcast',
      version='0.2',
      description='Receive and handle EVLA multicast messages',
      author='Paul Demorest',
      author_email='pdemores@nrao.edu',
      url='https://github.com/demorest/evla_mcast/',
      install_requires=['lxml', 'future'],
      packages=find_packages(exclude=('tests',)),
      package_data={'evla_mcast': ['xsd/*.xsd','xsd/vci/*.xsd','xsd/observe/*.xsd']},
     )
