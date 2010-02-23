#!/usr/bin/python -tt
# vim: ai ts=4 sts=4 et sw=4

#    Copyright (c) 2009 Intel Corporation
#
#    This program is free software; you can redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by the Free
#    Software Foundation; version 2 of the License
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
#    for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc., 59
#    Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import sys

# third-party modules
from termcolor import colored

__ALL__ = ['info', 'warning', 'error']

def info(msg):
    print >> sys.stderr, colored('Info:', 'white', on_color='on_blue'), msg

def warning(msg):
    print >> sys.stderr, colored('Warning:', 'yellow', on_color='on_blue'), msg

def error(msg):
    print >> sys.stderr, colored('Error:', 'red', on_color='on_blue'), msg
    sys.exit(1)

