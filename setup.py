#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)


import sys
import warnings
try:
    from setuptools import setup
except ImportError:
    try:
        from setuptools.core import setup
    except ImportError:
        from distutils.core import setup

from distutils.core import setup, Extension


setup(name='lupit',
      version='0.1',
      description='Scanning software cluged together',
      author='Stuart Wilkins',
      author_email='swilkins@bnl.gov',
      packages=['lupit'],
     )
