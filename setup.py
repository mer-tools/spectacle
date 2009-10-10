#!/usr/bin/env python

from distutils.core import setup

setup(name='spectacle',
      version='0.1',
      description='Spectacle',
      author='Anas Nashif',
      author_email='anas.nashif@intel.com',
      url='http://moblin.org/',
      scripts=['specify'],
      packages=['spectacle', 'spectacle.spec', 'spectacle.dsc'],
     )

