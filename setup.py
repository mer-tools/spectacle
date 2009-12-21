#!/usr/bin/env python

from distutils.core import setup

setup(name='spectacle',
      version='0.5',
      description='Spectacle',
      author='Anas Nashif, Jian-feng Ding',
      author_email='anas.nashif@intel.com, jian-feng.ding@intel.com',
      url='http://moblin.org/',
      scripts=['tools/specify', 'tools/ini2spectacle'],
      packages=['spectacle', 'spectacle.spec', 'spectacle.dsc'],
     )

