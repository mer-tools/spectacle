#!/usr/bin/env python

from distutils.core import setup

version_path = 'VERSION'
try:
    # first line should be the version number
    version = open(version_path).readline().strip()
    ver_file = open('spectacle/__version__.py', 'w')
    ver_file.write("version = \"%s\"\n" % version)
    ver_file.close()
except IOError:
    print 'WARNING: Cannot write version number file'
    pass

setup(name='spectacle',
      version = version,
      description='Spectacle',
      author='Anas Nashif, Jian-feng Ding',
      author_email='anas.nashif@intel.com, jian-feng.ding@intel.com',
      url='http://moblin.org/',
      scripts=['tools/specify', 'tools/ini2spectacle'],
      packages=['spectacle', 'spectacle.spec', 'spectacle.dsc'],
     )

