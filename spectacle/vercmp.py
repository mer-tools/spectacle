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

import re
import string
import distutils.version

class FairVersion(distutils.version.LooseVersion):
    """ Version schemes based on LooseVersion in distutils.version, but with
    more comparison rules to meet the expect result. For instance, the 'git',
    'rc', 'svn', 'beta' alphabetic components means "pre-release" tags, and
    other additional non-numberic identifiers means "post-release" tags.
    In the version comparison of the versions with extra tags, this rule will
    be applied:
      "pre-release" version < release version < "post-release" version
    e.g.:
      1.1.0git < 1.1.0 < 1.1.1 < 1.1.1-meego

    It can hardly cover all the special cases, but if the version string can
    follow the packaging guideline of MeeGo, this class is useful enough.
    """

    pre_tags = ('git', 'svn', 'cvs', 'alpha', 'a', 'beta', 'b', 'rc')

    def parse (self, vstring):
        self.vstring = vstring
        components = [x for x in self.component_re.split(vstring) if x and x != '.']

        numbers = []
        extras = []
        for part in components:
            if not extras:
                try:
                    numbers.append(int(part))
                except ValueError:
                    extras.append(part)
            else:
                extras.append(part)

        self.version = numbers
        self.extra_tags = extras

    def __repr__ (self):
        return "FairVersion ('%s')" % str(self)

    def __cmp__ (self, other):
        if isinstance(other, str):
            other = FairVersion(other)

        res = cmp(self.version, other.version)
        if res == 0:
            # need to consider the extra tags in
            if not self.extra_tags and not other.extra_tags:
                return 0

            self_pre = None
            self_post = None
            oth_pre = None
            oth_post = None
            if self.extra_tags:
                if self.extra_tags[0] in self.pre_tags:
                    self_pre = True
                else:
                    self_post = True
            if other.extra_tags:
                if other.extra_tags[0] in self.pre_tags:
                    oth_pre = True
                else:
                    oth_post = True

            if (self_pre and oth_pre) or (self_post and oth_post):
                return cmp(self.extra_tags, other.extra_tags)

            elif self_pre and not oth_pre:
                return -1
            elif oth_post:
                return -1
            elif oth_pre or self_post:
                return 1

            # must not reach here!!
            raise ValueError()
        else:
            return res


if __name__ == '__main__':
    # test cases
    import pprint

    vers = ['1.1.0',
            '1.1',
            '1.0',
            '1.1git',
            '1.1-meego',
            '1.1.0git',
            '1.1.0meego1',
            '1.1.0meego2',
            '1.1.0.1',
            '1.1.1']
    fvers = [FairVersion(v) for v in vers]
    fvers.sort()
    pprint.pprint(fvers)

