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

import os,sys


__ALL__ = ['info', 'warning', 'error', 'ask']

# COLORs in ANSI
INFO_COLOR = 32 # green
WARN_COLOR = 33 # yellow
ERR_COLOR  = 31 # red
ASK_COLOR  = 34 # blue

def _color_print(head, color, msg = None, stream = sys.stdout):
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        head = '\033[%dm%s:\033[0m' %(color, head)
    if msg:
        print >> stream, head, msg
    else:
        print >> stream, head,

def _color_perror(head, color, msg):
    _color_print(head, color, msg, sys.stderr)

def info(msg):
    _color_perror('Info', INFO_COLOR, msg)

def warning(msg):
    _color_perror('Warning', WARN_COLOR, msg)

def error(msg):
    _color_perror('Error', ERR_COLOR, msg)
    sys.exit(1)

def ask(msg):
    _color_print('Q', ASK_COLOR, '')
    try:
        return raw_input(msg)
    except KeyboardInterrupt:
        print
        sys.exit(2)

