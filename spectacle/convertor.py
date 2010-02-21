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
                 'Epoch',
                 'Group',
                 'License',
                 'URL',
                 'Sources',
                 'ExtraSources',
                 'Patches',
                 'Description',
                 '',
                 'Requires',
                 'RequiresPre',
                 'RequiresPreUn',
                 'RequiresPost',
                 'RequiresPostUn',
                 'PkgBR',
                 'PkgConfigBR',
                 'Provides',
                 'Obsoletes',
                 'Conflicts',
                 'Configure',
                 'ConfigOptions',
                 'Builder',
                 'BuildArch',
                 'LocaleName',
                 'LocaleOptions',
                 'NeedCheckSection',
                 'SupportOtherDistros',
                 'UseAsNeeded',
                ]

EXTRA_ENTRIES = ['Files',
                 'PostMakeExtras',
                 'PostMakeInstallExtras',
                ]

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

    def _remove_duplicate(self, dict):
        # check duplicate default configopts
        dup = '--disable-static'
        if 'ConfigOptions' in dict and dup in dict['ConfigOptions']:
            dict['ConfigOptions'].remove(dup)
            if not dict['ConfigOptions']:
                del dict['ConfigOptions']

        # check duplicate requires for base package
        if "SubPackages" in dict:
            if 'Epoch' in dict:
                autodep = "%{name} = %{epoch}:%{version}-%{release}"
            else:
                autodep = "%{name} = %{version}-%{release}"

            for sp in dict["SubPackages"]:
                if 'Requires' in sp and autodep in sp['Requires']:
                    sp['Requires'].remove(autodep)
                    if not sp['Requires']:
                        del sp['Requires']

        # check duplicate '%defattr' for files list
        if 'extra' in dict and 'Files' in dict['extra']:
            try:
                dict['extra']['Files'].remove('%defattr(-,root,root,-)')
            except ValueError:
                pass

    def convert(self, dict, need_break = True):
        self._replace_keys(dict)
        self._remove_duplicate(dict)

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
                print >> sys.stderr, 'Warning: need to remove this key to extra', entry
                extra[entry] = dict[entry]
                del dict[entry]

        if 'extra' in dict:
            extra.update(dict['extra'])
            del dict['extra']

        for k, v in dict.iteritems():
            print >> sys.stderr, 'Warning: un-ordered entry: %s\n' % (k)
            items.append((k, v))

        if extra:
            try:
                # clean up empty lines
                files = [s.strip() for s in extra['Files'] if s.strip()]
                if files:
                    extra['Files'] = files
                else:
                    del extra['Files']
            except KeyError:
                pass

            if extra: # check it again
                items.append(('extra', extra))

        if subpkgs:
            items.append(('SubPackages', subpkgs))

        return items
