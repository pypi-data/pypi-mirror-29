#!/usr/bin/env python

#import os
import setuptools
from distutils.core import setup

setup(
  name='iRep',
  packages = ['iRep'],
  scripts = ['iRep/iRep', 'iRep/bPTR', 'iRep/gc_skew.py', 'iRep/iRep_filter.py'],
  version='1.1.14',
  description='calculate iRep replication rates from metagenome sequencing',
  author='Chris Brown',
  author_email='ctb@berkeley.edu',
  license='MIT',
  url='https://github.com/christophertbrown/iRep',
  install_requires=['lmfit', 'numpy', 'scipy', 'pandas', \
                    'seaborn', 'matplotlib', 'ctbBio'],
  classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3'
  ]
)
