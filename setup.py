#!/usr/bin/env python
# ***************************************************************************
# Copyright (c) 2018 SAP SE or an SAP affiliate company. All rights reserved.
# ***************************************************************************

r"""sqlanydb - pure Python SQL Anywhere database interface.

sqlanydb lets one access and manipulate SQL Anywhere databases
in pure Python.

https://github.com/sqlanywhere/sqlanydb

----------------------------------------------------------------"""

from setuptools import setup, find_packages
import os,re

with open( os.path.join( os.path.dirname(__file__), 'sqlanydb.py' ) ) as v:
    VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)

setup(name='sqlanydb',
      version=VERSION,
      description='pure Python SQL Anywhere database interface',
      long_description=open('README.rst').read(),
      author='Graeme Perrow',
      author_email='graeme.perrow@sap.com',
      url='https://github.com/sqlanywhere/sqlanydb',
      packages=find_packages(),
      py_modules=['sqlanydb'],
      license='Apache 2.0',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
     )
