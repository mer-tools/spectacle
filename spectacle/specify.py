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

import os, sys
import re
import tempfile
import shutil
import copy

# third-party modules
import yaml

# internal modules
import spec

class GitAccess():
    def __init__(self, path):
        self.path = path
    def gettags(self):
          tags = {}
          fh = os.popen('git ls-remote --tags "%s" 2>/dev/null' % self.path)
          prefix = 'refs/tags/'
          for line in fh:
              line = line.strip()
              node, tag = line.split(None, 1)
              if not tag.startswith(prefix):
                  continue
              tagx = tag[len(prefix):len(tag)]
              tags[tagx] = node
          return tags

class RPMWriter():
    extra_per_pkg = {
                        'PreUn': [],
                        'Desktop': False,
                        'Static': False,
                        'Schema': False,
                        'Schemas': [],
                        'Lib': False,
                        'Icon': False,
                        'Service': False,
                        'Info': False,
                        'Infos': [],
                    }

    extra = {
                'subpkgs':  {},
                'content': {},
            }

    def __init__(self,  filename, clean_old = False):
        self.filename = filename
        self.metadata = None
        self.scm = None
        self.pkg = None
        self.specfile = None
        self.version = None

        self.clean_old = clean_old

        # update extra info for main package
        self.extra.update(copy.deepcopy(self.extra_per_pkg))

        try:
            self.stream = file(filename, 'r')
        except IOError:
            print 'Cannot file %s for read.' % filename
            sys.exit(1)

    def dump(self):
        print yaml.dump(yaml.load(self.stream))

    def parse(self):
        self.metadata = yaml.load(self.stream)
        if self.metadata.has_key("SCM"):
            self.scm = self.metadata['SCM']

        try:
            self.pkg = self.metadata['Name']
            self.specfile = "%s.spec" % self.pkg

            self.newspec = True

            if os.path.exists(self.specfile):
                if self.clean_old:
                    os.rename(self.specfile, self.specfile + '.bak')
                else:
                    self.newspec = False

        except KeyError:
            print 'Invalid yaml file %s without "Name" directive' % self.filename
            sys.exit(1)

        if self.metadata.has_key("SubPackages"):
            for sp in self.metadata["SubPackages"]:
                self.extra['subpkgs'][sp['Name']] = copy.deepcopy(self.extra_per_pkg)

        #if self.metadata.has_key("SubPackages"):
        #    self.metadata["sp"] = []
        #    for sp in self.metadata["SubPackages"]:
        #        self.metadata["sp"].append(self.metadata[sp])

    def parse_files(self, files = {}):
        for pkg_name,v in files.iteritems():

            if pkg_name == 'main':
                pkg_extra = self.extra
            else:
                pkg_extra = self.extra['subpkgs'][pkg_name]

            for l in v:
                if re.match('.*\.info.*', l) and re.match('.*usr/share/info.*', l):
                    pkg_extra['PreUn'].append("/sbin/install-info")
                    pkg_extra['Infos'].append(l)
                    pkg_extra['Info'] = True
                if re.match('.*\.desktop$', l):
                    pkg_extra['Desktop'] = True
                if re.match('.*\.a$', l):
                    pkg_extra['Static'] = True
                if re.match('.*etc/rc.d/init.d.*', l) or re.match('.*etc/init.d.*', l):
                    pkg_extra['Service'] = True
                    pkg_extra['PreUn'].append("/sbin/chkconfig")
                    pkg_extra['PreUn'].append("/sbin/service")
                if re.match('.*%{_libdir}.*', l) or re.match('.*\.so\..*', l):
                    pkg_extra['Lib'] = True
                if re.match('.*\.schema.*', l):
                    pkg_extra['Schema'] = True
                    pkg_extra['Schemas'].append(l)
                if re.match('.*\/icons\/.*', l):
                    pkg_extra['Icon'] = True

    def parse_existing(self, filename):
        sin = re.compile("^# >> ([^\s]+) (.*)")
        sout = re.compile("^# << ([^\s]+) (.*)")
        recording = []
        record = False
        files = {}
        install = {}
        build = {}
        for i in file(filename).read().split("\n"):
            matchin = sin.match(i)
            matchout = sout.match(i)
            if matchin:
                record = True
                recording = []
                continue
            if matchout:
                record = False
                if matchout.group(1) == "files" and not matchout.group(2):
                    files['main'] = recording
                elif matchout.group(1) == "files" and matchout.group(2):
                    files[matchout.group(2)] = recording
                elif matchout.group(1) == "install":
                    install[matchout.group(2)] = recording
                elif matchout.group(1) == "build":
                    build[matchout.group(2)] = recording

            if record:
                recording.append(i)

        return { "files" : files,
                 "install": install,
                 "build" : build
               }

    def process(self, extra):
        specfile = self.specfile
        if not self.newspec:
            self.extra['content'] = self.parse_existing(specfile)

        if extra:
            self.extra.update(extra)

        try:
            self.parse_files(self.extra['content']['files'])
        except KeyError:
            pass

        #import pprint
        #pprint.pprint(self.metadata)
        #pprint.pprint(self.extra)

        spec_content = str(
                spec.spec(searchList=[{
                                        'metadata': self.metadata,
                                        'extra': self.extra
                                      }]))

        file = open(specfile, "w")
        file.write(spec_content)
        file.close()

def generate_rpm(filename, clean_old = False, extra = None):
    rpm = RPMWriter(filename, clean_old)
    rpm.parse()
    if rpm.scm is not None:
        scm = GitAccess(rpm.scm)
        print "Getting tags from SCM..."
        tags = scm.gettags()
        if len(tags) > 0:
            rpm.version = sorted(tags.keys())[-1]
            rpm.metadata['Version'] = rpm.version
            tmp = tempfile.mkdtemp()
            pwd = os.getcwd()
            os.chdir(tmp)
            print "Creating archive %s/%s-%s.tar.bz2 ..." %( pwd, rpm.pkg, rpm.version )
            os.system('git clone %s' %rpm.scm)
            os.chdir( "%s/%s" %(tmp, rpm.pkg))
            os.system(' git archive --format=tar --prefix=%s-%s/ %s | bzip2  > %s/%s-%s.tar.bz2' %(rpm.pkg, rpm.version, rpm.version, pwd, rpm.pkg, rpm.version ))
            shutil.rmtree(tmp)
            os.chdir(pwd)

    rpm.process(extra)

    return rpm.specfile, rpm.newspec
