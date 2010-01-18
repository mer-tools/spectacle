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

ORDER_ENTRIES = ['Name',
                 'Summary',
                 'Version',
                 'Release',
                 'Group',
                 'License',
                 'URL',
                 'Description',
                 '',
                 'Sources',
                 'Patches',
                 '',
                 'Requires',
                 'PkgBR',
                 'PkgConfigBR',
                 'Provides',
                 'Obsoletes',
                 'Conflicts',
                 'Configure',
                 'ConfigOptions',
                 'Builder',
                 'Documents',
                 'LocaleName',
                ]

EXTRA_ENTRIES = ['Files',
                 'PostMakeInstallExtras',
                ]

# TODO, move 'files', 'extra scripts' to extra

class Convertor(object):
    """ Class for generic operations:
        *   Translate field names between different format
        *   Transfer non-order dict to ordered list of (key, val) pairs

        Derived sub-classes should update cv_table, the dictionary for
        translation, for specific input format.
    """

    cv_table = {}

    # un-ordered ones will be append the ordered ones in random order
    # 'Files', 'SubPackages' will the last two

    def __init__(self, cv_table = {}):
        self.cv_table.update(cv_table)

    def _replace_keys(self, dict):
        for k,v in self.cv_table.iteritems():
            if k in dict:
                dict[v] = dict[k]
                del dict[k]

    def convert(self, dict, need_break = True):
        self._replace_keys(dict)

        items = []
        for entry in ORDER_ENTRIES:
            if not entry:
                # empty string means a blank line for break
                if need_break:
                    items.append(('', ''))
                continue

            if entry in dict:
                items.append((entry, dict[entry]))
                del dict[entry]

        subpkgs = []
        try:
            subpkgs_list = dict['SubPackages']
            del dict['SubPackages']

            for sub_items in subpkgs_list:
                subpkgs.append(self.convert(sub_items, False))
        except:
            pass

        extra = {}
        for entry in EXTRA_ENTRIES:
            if entry in dict:
                extra[entry] = dict[entry]
                del dict[entry]

        if 'extra' in dict:
            extra.update(dict['extra'])
            del dict['extra']

        for k, v in dict.iteritems():
            print >> sys.stderr, 'DEBUG: un-ordered entry: %s\n' % (k)
            items.append((k, v))

        if extra:
            items.append(('extra', extra))

        if subpkgs:
            items.append(('SubPackages', subpkgs))

        return items
