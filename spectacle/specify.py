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
    def __init__(self,  filename):
        self.filename = filename
        self.stream = file(filename, 'r')
        self.metadata = None
        self.scm = None
        self.pkg = None
        self.version = None
        self.extra = {}
        pass
    def dump(self):
        print yaml.dump(yaml.load(self.stream))
    def parse(self):
        self.metadata = yaml.load(self.stream)
        if self.metadata.has_key("SCM"):
            self.scm = self.metadata['SCM']
        if self.metadata.has_key("Name"):
            self.pkg = self.metadata['Name']

        #if self.metadata.has_key("SubPackages"):
        #    self.metadata["sp"] = []
        #    for sp in self.metadata["SubPackages"]:
        #        self.metadata["sp"].append(self.metadata[sp])
        
    def parse_files(self, files = {}):
        self.extra = {
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
        for k,v in files.iteritems():
            for l in v:
                if re.match('.*\.info.*', l) and re.match('.*usr/share/info.*', l):
                    self.extra['PreUn'].append("/sbin/install-info")
                    self.extra['Infos'].append(l)
                    self.extra['Info'] = True
                if re.match('.*\.desktop$', l):
                    self.extra['Desktop'] = True
                if re.match('.*\.a$', l):
                    self.extra['Static'] = True
                if re.match('.*etc/rc.d/init.d.*', l) or re.match('.*etc/init.d.*', l):
                    self.extra['Service'] = True
                    self.extra['PreUn'].append("/sbin/chkconfig")
                    self.extra['PreUn'].append("/sbin/service")
                if re.match('.*\.so\..*', l):
                    self.extra['Lib'] = True
                if re.match('.*\.schema.*', l):
                    self.extra['Schema'] = True
                    self.extra['Schemas'].append(l)


    def parse_existing(self, file = None):
        sin = re.compile("^# >> ([^\s]+) (.*)")
        sout = re.compile("^# << ([^\s]+) (.*)")
        recording = []
        record = False
        files = {}
        install = {}
        build = {}
        for i in file.read().split("\n"):  
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
        usercontent = {"files" : files, "install": install, "build" : build}
        return usercontent

    def process(self):
        specfile = "%s.spec" %self.metadata['Name']
        if os.path.exists(specfile):
            print "file exists, patching..."
            file = open(specfile, "r")
            usercontent = self.parse_existing(file)
            file.close()
            self.parse_files(usercontent['files'])
            self.extra['content'] = usercontent
            nameSpace = {'metadata': self.metadata, 'extra': self.extra }
            t = spec.spec(searchList=[nameSpace])
            a = str(t)
            file = open(specfile, "w")
            file.write(a)
            file.close()           
        else:
            print "Creating new spec file: %s" %specfile
            self.parse_files()
            self.extra['content'] = {}
            nameSpace = {'metadata': self.metadata, 'extra': self.extra }
            t = spec.spec(searchList=[nameSpace])
            a = str(t)
            file = open(specfile, "w")
            file.write(a)
            file.close()

        #t = dsc(searchList=[nameSpace])
        #a = str(t)
        #print a

def generate_rpm(args):
    for filename in args[1:]:
        rpm = RPMWriter(filename)
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

        rpm.process()

    return 0
