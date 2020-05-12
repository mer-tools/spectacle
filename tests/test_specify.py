#!/usr/bin/python3
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
import glob
import tempfile
import subprocess
import unittest

from testbase import *

class TestSpecifyKeys(unittest.TestCase):
    cases_dir = 'specify_cases'

    # build cases on the fly based on directories
    if os.path.isdir(cases_dir):
        for case in glob.glob(os.path.join(cases_dir, 'test-*')):
            if not os.path.exists(os.path.join(case, 'input.p')):
                continue
            case = os.path.basename(case)[5:]
            newmethod = """
def test_%s(self):
    print("case %s ok")
    self.assertTrue(self._compare_out_file("%s"))
""" % (case, case, case)
            exec(newmethod, locals())

    def _compare_out_file(self, case):
        prep_working_env(self.cases_dir, case, self.work_dir)

        if run_and_check(self.work_dir):
            return (compare_outfile(self.work_dir))
        else:
            return False

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()

    def tearDown(self):
        cleanup(self.work_dir)

def suite():
    tl = unittest.TestLoader()
    return tl.loadTestsFromModule(sys.modules[__name__])
