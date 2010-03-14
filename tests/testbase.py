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

SCRIPTS = """
specify -N -o output.spec testpkg.yaml 1>output.1 2>output.2
mv output.spec output.orig.spec
patch -s < input.p
specify -N -o output.spec testpkg.yaml 1>newouput.1 2>newoutput.2
if [ ! -f output.no -a ! -f output.spec ]; then
  mv newoutput.2 output.error
  exit 1
fi
if [ -f output.p ]; then
  diff output.orig.spec output.spec > newoutput.p
fi
if [ -f output.1p ]; then
  diff output.1 newoutput.1 > newoutput.1p
fi
if [ -f output.2p ]; then
  diff output.2 newoutput.2 > newoutput.2p
fi
"""

import os,sys
import glob
import shutil

def prep_working_env(cases_dir, case, dst_dir):
    shutil.copy(os.path.join(cases_dir, 'base', 'testpkg.yaml'), dst_dir)
    for out in glob.glob(os.path.join(cases_dir, 'test-'+case, '*')):
        try:
            if not os.path.isdir(out):
                shutil.copy(out, dst_dir)
        except:
            pass # ignore if file missing

def cleanup(work_dir):
    shutil.rmtree(work_dir)

def run_and_check(work_dir):
    result = True
    cwd = os.getcwd()
    os.chdir(work_dir)
    os.system(SCRIPTS)
    if os.path.exists('output.error'):
        # something wrong with tested tools
        print >> sys.stderr, file(os.path.join(work_dir, 'output.error')).read()
        result = False

    os.chdir(cwd)
    return result

def compare_outfile(work_dir):
    all_equ = True
    #print glob.glob(os.path.join(work_dir, '*'))
    for out in ('output.p', 'output.1p', 'output.2p'):
        fp = os.path.join(work_dir, out)
        if os.path.exists(fp):
            exp_output_diff = file(fp).read().strip()
            output_diff = file(os.path.join(work_dir, 'new'+out)).read().strip()
            """
            print fp, 'orig>>>'
            print exp_output_diff
            print fp, 'new<<<'
            print output_diff
            """
            all_equ = all_equ and (exp_output_diff == output_diff)

    return all_equ
