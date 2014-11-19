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


# create ipython "lupit" profile
import os
from subprocess import call
import IPython

profile_name = 'lupit'
call('ipython profile create {}'.format(profile_name), shell=True)
ipython_version = IPython.version_info

# if ipython_version[0] == 2:
#
# else:
if ipython_version[0] == 2:
    config_path = os.path.expanduser('~/.ipython')
else:
    config_path = os.path.expanduser('~/.config/ipython')

config_path += "/profile_{}/ipython_config.py".format(profile_name)

new_ipython_config =(
    "# Configuration file for ipython."
    "\nc = get_config()"
    "\n"
    "\n# Pre-load matplotlib and numpy for interactive use, selecting a particular"
    "\n# matplotlib backend and loop integration."
    "\nc.InteractiveShellApp.pylab = 'auto'"
    "\n"
    "\n# If true, IPython will populate the user namespace with numpy, pylab, etc. and"
    "\n# an 'import *' is done from numpy and pylab, when using pylab mode."
    "\n# When False, pylab mode should not import any names into the user namespace."
    "\nc.InteractiveShellApp.pylab_import_all = True"
    "\n"
    "\n# A list of dotted module names of IPython extensions to load."
    "\nc.InteractiveShellApp.extensions = ["
    "\n    'autoreload',"
    "\n    'lupit.ipy'"
    "\n]"
    "\n"
    "\n# lines of code to run at IPython startup."
    "\nc.TerminalIPythonApp.exec_lines = ["
    "\n    'from epics import caget, caput, camonitor, PV',"
    "\n    '%autoreload 2',"
    "\n    'from epicsscan import *',"
    "\n    'from lupit import *'"
    "\n]"
)

print('new ipython config: {}'.format(new_ipython_config))

print('config_path: {}'.format(config_path))

with open(config_path, 'w') as file:
    file.write(new_ipython_config)