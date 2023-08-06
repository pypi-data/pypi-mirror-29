# -*- coding: utf-8 -*-

import io
import sys
import numpy as np
from setuptools import find_packages
from setuptools import setup
from ct_manager import __version__

PACKAGE = 'ct_manager'
NAME = 'ct_manager'
VERSION = __version__
DESCRIPTION = 'data manager'
AUTHOR = 'iLampard, MarkSh714, Bella21'
URL = 'https://github.com/iLampard/ct_manager'
LICENSE = 'Apache'

if sys.version_info > (3, 0, 0):
    requirements = "requirements/py3.txt"
else:
    requirements = "requirements/py2.txt"

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      url=URL,
      data_files=[('config', ['ct_manager/config.yaml'])],
      include_package_data=True,
      packages=find_packages(),
      install_requires=io.open(requirements, encoding='utf8').read(),
      include_dirs=[np.get_include()],
      classifiers=['Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6'])
