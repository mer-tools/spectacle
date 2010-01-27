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
import __version__
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
    """
        The following keys will be generated on the fly based on values from
        YAML, and transfered to tmpl:
            MyVersion:    version of spectacle
            ExtraInstall: extra install script for 'ExtraSources'
            BuildingPath: path for rpm 'setup' macro

    """

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

    def __init__(self, yaml_fpath, clean_old = False):
        self.yaml_fpath = yaml_fpath
        self.metadata = {'MyVersion': __version__.version}
        self.scm = None
        self.archive = 'bzip2'
        self.pkg = None
        self.specfile = None

        self.clean_old = clean_old

        # initialize extra info for spec
        self.extra = { 'subpkgs': {}, 'content': {} }

        # update extra info for main package
        self.extra.update(copy.deepcopy(self.extra_per_pkg))

        # record filelist from 'ExtraSources' directive
        self.extras_filelist = []

        try:
            self.stream = file(yaml_fpath, 'r')
        except IOError:
            print 'Cannot read file: %s' % yaml_fpath
            sys.exit(1)

    def dump(self):
        print yaml.dump(yaml.load(self.stream))

    def parse(self):

        # customized Resolver for Loader, in PyYAML
        # remove all resolver for 'int' and 'float', handle them as str
        for ch in u'+-1234567890.':
            if ch in yaml.loader.Loader.yaml_implicit_resolvers:
                for tp in yaml.loader.Loader.yaml_implicit_resolvers.get(ch):
                    if tp[0] == u'tag:yaml.org,2002:float':
                        yaml.loader.Loader.yaml_implicit_resolvers.get(ch).remove(tp)
                for tp in yaml.loader.Loader.yaml_implicit_resolvers.get(ch):
                    if tp[0] == u'tag:yaml.org,2002:int':
                        yaml.loader.Loader.yaml_implicit_resolvers.get(ch).remove(tp)

        self.metadata.update(yaml.load(self.stream))

        # handling 'ExtraSources', extra separated files which need to be install
        # specific paths
        if self.metadata.has_key("ExtraSources"):
            extra_srcs = []
            extra_install = ''
            count = len(self.metadata['Sources'])
            for extra_src in self.metadata['ExtraSources']:
                try:
                    file, path = map(str.strip, extra_src.split(';'))
                except:
                    file = extra_src.strip()
                    path = ''
                self.extras_filelist.append(os.path.join(path, file))

                extra_srcs.append(file)
                if path:
                    extra_install += "mkdir -p %%{buildroot}%s\n" % (path)
                extra_install += "cp -a %%{SOURCE%s} %%{buildroot}%s\n" % (count, path)
                count = count + 1

            self.metadata['Sources'].extend(extra_srcs)
            self.metadata['ExtraInstall'] = extra_install

        if self.metadata.has_key("SCM"):
            self.scm = self.metadata['SCM']

        supported_archive = ['bzip2', 'gzip']
        if self.metadata.has_key("Archive"):
            self.archive = self.metadata['Archive']
            if self.archive not in supported_archive:
                self.archive = 'bzip2'
        if self.archive == 'bzip2':
            self.appendix = 'bz2'
        else:
            self.appendix = 'gz'

        try:
            dirname, ignore = os.path.basename(self.metadata['Sources'][0]).split('.tar.')
            self.metadata['BuildingPath'] = dirname
        except:
            self.metadata['BuildingPath'] = self.metadata['Name']

        try:
            self.pkg = self.metadata['Name']
            self.specfile = "%s.spec" % self.pkg

            self.newspec = True

            if os.path.exists(self.specfile):
                if self.clean_old:
                    # backup original file
                    bak_spec_fpath = self.specfile + '.orig'
                    if os.path.exists(bak_spec_fpath):
                        repl = raw_input('%s will be overwritten by the backup, continue?(Y/n) ' % bak_spec_fpath)
                        if repl == 'n':
                            sys.exit(1)

                    os.rename(self.specfile, bak_spec_fpath)
                else:
                    self.newspec = False

        except KeyError:
            print 'Invalid yaml file %s without "Name" directive' % self.yaml_fpath
            sys.exit(1)

        if self.metadata.has_key("SubPackages"):
            for sp in self.metadata["SubPackages"]:
                self.extra['subpkgs'][sp['Name']] = copy.deepcopy(self.extra_per_pkg)

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
                if re.match('.*%{_libdir}.*', l) and re.match('.*\.so.*', l) and pkg_name != 'devel':
                    # 'devel' sub pkgs should not set Lib flags
                    pkg_extra['Lib'] = True
                if re.match('.*\.schema.*', l):
                    pkg_extra['Schema'] = True
                    pkg_extra['Schemas'].append(l)
                if re.match('.*\/icons\/.*', l):
                    pkg_extra['Icon'] = True

    def parse_existing(self, spec_fpath):
        sin = re.compile("^# >> ([^\s]+) (.*)")
        sout = re.compile("^# << ([^\s]+) (.*)")
        recording = []
        record = False
        files = {}
        install = {}
        build = {}
        macros = {}
        for i in file(spec_fpath).read().split("\n"):
            matchin = sin.match(i)
            matchout = sout.match(i)
            if matchin:
                record = True
                recording = []
                continue
            if matchout:
                record = False
                if not recording: continue # empty

                if matchout.group(1) == "files" and not matchout.group(2):
                    files['main'] = recording
                elif matchout.group(1) == "files" and matchout.group(2):
                    files[matchout.group(2)] = recording
                elif matchout.group(1) == "install":
                    install[matchout.group(2)] = recording
                elif matchout.group(1) == "build":
                    build[matchout.group(2)] = recording
                elif matchout.group(1) == "macros":
                    macros['main'] = recording

            if record:
                recording.append(i)

        return { "files" : files,
                 "install": install,
                 "build" : build,
                 "macros" : macros
               }

    def process(self, extra_content):
        specfile = self.specfile
        if not self.newspec:
            self.extra['content'] = self.parse_existing(specfile)

        if extra_content:
            self.extra['content'].update(extra_content)

        """
        TODO: should not regard them as the content of MAIN pkg
        if self.extras_filelist:
            try:
                self.extra['content']['files']['main'].extend(self.extras_filelist)
            except KeyError:
                self.extra['content'].update({'files': {'main': self.extras_filelist}})
        """

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

def get_scm_latest_release(rpm):
    scm = GitAccess(rpm.scm)
    print "Getting tags from SCM..."
    tags = scm.gettags()
    if len(tags) > 0:
        rpm.version = sorted(tags.keys())[-1]
        rpm.metadata['Version'] = rpm.version
        tmp = tempfile.mkdtemp()
        pwd = os.getcwd()
        if os.path.exists("%s/%s-%s.tar.%s" %(pwd, rpm.pkg, rpm.version, rpm.appendix )):
            print "Archive already exists, not creating a new one"
        else:
            print "Creating archive %s/%s-%s.tar.%s ..." %( pwd, rpm.pkg, rpm.version, rpm.appendix )
            os.chdir(tmp)
            os.system('git clone %s' %rpm.scm)
            os.chdir( "%s/%s" %(tmp, rpm.pkg))
            os.system(' git archive --format=tar --prefix=%s-%s/ %s | %s  > %s/%s-%s.tar.%s' %(rpm.pkg, rpm.version, rpm.version, rpm.archive, pwd, rpm.pkg, rpm.version, rpm.appendix ))
        shutil.rmtree(tmp)
        os.chdir(pwd)

def download_sources(pkg, rev, sources):
    def _dl_progress(count, s_block, s_total):
        percent = int(count * s_block*100 / s_total)
        if percent > 100: percent = 100
        sys.stdout.write('\r... %d%%' % percent)
        if percent == 100: print ' Done.'

        sys.stdout.flush()

    for s in sources:
        if s.startswith('http://') or s.startswith('ftp://'):
            target = s.replace('%{name}', pkg)
            target = target.replace('%{version}', rev)
            f_name = os.path.basename(target)
            if not os.path.isfile(f_name):
                repl = raw_input('Need to download source package: %s ?(Y/n) ' % f_name)
                if repl == 'n': break

                print 'Downloading latest source package from:', target
                import urllib
                urllib.urlretrieve(target, f_name, reporthook = _dl_progress)
                """
                for ext in ('.md5', '.gpg', '.sig', '.sha1sum'):
                    urllib.urlretrieve(target + ext, f_name + ext)
                """

def generate_rpm(yaml_fpath, clean_old = False, extra_content = None):
    rpm = RPMWriter(yaml_fpath, clean_old)
    rpm.parse()

    # update to SCM latest release
    if rpm.scm is not None:
        get_scm_latest_release(rpm)

    # if no srcpkg with yaml.version exists in cwd, trying to download
    download_sources(rpm.pkg, rpm.metadata['Version'], rpm.metadata['Sources'])

    rpm.process(extra_content)

    return rpm.specfile, rpm.newspec
