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

TAB = '    ' # 4space, instead of Tab

class SpectacleDumper(object):
    """ Dumper medium data to output format.
        Supported output format:
            yaml, json

        The format of medium data of spectacle, as input for dumping:
        data = [
                 (key1, val1),
                 ('', '')                       # for blank line
                 (key2, [val21, val22, val23])
                 (key3, [
                          [
                            (key31, val31),
                            (key32, val32),
                            ...
                          ],
                          [
                            ...
                          ],
                        ])
               ]

    """

    spec_extra_keys = {
            # key -> ( nkey, nsubkey)
            #                ^^ None means to use <pkg_name>
            'Files': ('files', None),
            'PostMakeInstallExtras': ('install', 'post'),
            'PreMakeInstallExtras': ('install', 'pre'),
            }

    def __init__(self, format = 'yaml', opath = None):
        self.format = format
        self.opath = opath

        self.spec_extra = {}

    def _dump_json(self, data):
        import json
        print json.dumps(data, indent=4)

    def __esc_value(self, val):
        # ESC for leading '%', for yaml syntax
        if val.startswith('%'):
            return '"' + val + '"'
        else:
            return val

    def _dump_yaml(self, data, fp, indent = '', cur_pkg = 'main'):
        if indent:
            cur_indent = indent + '- '
        else:
            cur_indent = indent

        first_line = True
        for key, value in data:
            if not first_line and indent:
                cur_indent = indent + '  '

            if not key:
                # empty key means blank line for break
                fp.write("\n")
                continue

            if key in self.spec_extra_keys:
                nkey    = self.spec_extra_keys[key][0]
                nsubkey = self.spec_extra_keys[key][1]
                if not nsubkey:
                    nsubkey = cur_pkg
                if not isinstance(value, list):
                    value = [value]

                if nkey not in self.spec_extra:
                    self.spec_extra[nkey] = {}
                self.spec_extra[nkey][nsubkey] = value

                continue

            if isinstance(value, list):
                fp.write(cur_indent + "%s:\n" % (key))

                for item in value:
                    if isinstance(item, list):
                        # only 'SubPackges' will reach here
                        # cur_pkg will be the 1st pair  ('Name', subpkg)
                        self._dump_yaml(item, fp, cur_indent + TAB, cur_pkg = item[0][1])
                        fp.write("\n")
                    else:
                        fp.write(cur_indent + TAB + "- %s\n" % (self.__esc_value(item)))
            else:
                lines_to_write = value.splitlines()

                if len(lines_to_write) == 1:
                    fp.write(cur_indent + "%s: %s\n" % (key, self.__esc_value(value)))
                elif len(lines_to_write) == 0:
                    # not exist until now
                    fp.write(cur_indent + "%s:\n" % (key))
                else:
                    fp.write(cur_indent + "%s: |\n" % key)
                    for line in lines_to_write:
                        fp.write(cur_indent + TAB + "%s\n" % line)

            first_line = False

    def _update_spec(self):
        import specify
        return specify.generate_rpm(self.opath, True, self.spec_extra) [0]

    def dump(self, data, format = None):
        if not format:
            format = self.format

        fp = sys.stdout
        if self.opath:
            try:
                fp = file(self.opath, 'w')
            except IOError:
                print 'Cannot open file %s for writing' % self.opath
                # print out
                pass

        try:
            if format == 'yaml':
                self._dump_yaml(data, fp)
            elif format == 'json':
                self._dump_json(data)
        finally:
            fp.close()

        if self.spec_extra and self.opath:
            return self._update_spec()

        return None

