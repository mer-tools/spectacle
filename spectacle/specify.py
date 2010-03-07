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
import distutils.version as _V
import datetime
import csv
import tarfile


# third-party modules
import yaml

# internal modules
import __version__
import spec
import logger

SERIES_PATH = 'series.conf'

MAND_KEYS = ('Name',
             'Summary',
             'Version',
             'Group',
             'License',
            )

SUB_MAND_KEYS = ('Name',
                 'Summary',
                 'Group',
                )

BOOL_KEYS = ('NeedCheckSection',
             'SupportOtherDistros',
             'NoAutoReq',
             'NoAutoProv',
             'NoSetup',
             'UseAsNeeded',
            )

LIST_KEYS = ('Sources',
             'ExtraSources',
             'Patches',
             'Requires',
             'RequiresPre',
             'RequiresPreUn',
             'RequiresPost',
             'RequiresPostUn',
             'PkgBR',
             'PkgConfigBR',
             'Provides',
             'Conflicts',
             'Obsoletes',
             'AutoSubPackages',
             'Files',
             'Documents',
             )

STR_KEYS =  ('Name',
             'Summary',
             'Description',
             'Version',
             'Release',
             'Epoch',
             'Group',
             'License',
             'URL',
             'BuildArch',
             'ExclusiveArch',
             'SourcePrefix',
             'Configure',
             'Builder',
             'SetupOptions',
             'LocaleName',
             'LocaleOptions',
            )

class GitAccess():
    def __init__(self, path):
        self.path = path

    def _gettags(self):
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

    def get_toptag(self):
        vers = [_V.LooseVersion(tag) for tag in self._gettags()]
        if vers:
            vers.sort()
            return str(vers[-1])

        return None

class RPMWriter():
    """
        The following keys will be generated on the fly based on values from
        YAML, and transfered to tmpl:
            MyVersion:    version of spectacle
            ExtraInstall: extra install script for 'ExtraSources'

    """

    extra_per_pkg = {
                        'Desktop': False,
                        'Static': False,
                        'Schema': False,
                        'Schemas': [],
                        'Lib': False,
                        'HasStatic': False,
                        'Icon': False,
                        'Service': False,
                        'Info': False,
                        'Infos': [],
                    }

    def __init__(self, yaml_fpath, clean_old = False):
        self.yaml_fpath = yaml_fpath
        now = datetime.datetime.now()
        self.metadata = {'MyVersion': __version__.VERSION, 'Date': now.strftime("%Y-%m-%d")}
        self.pkg = None
        self.version = None
        self.release = None
        self.specfile = None
        self.packages = {}

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
            logger.error('Cannot read file: %s' % yaml_fpath)

    def dump(self):
        print yaml.dump(yaml.load(self.stream))
            
    def sanity_check(self):

        def _check_mandatory_keys(metadata, subpkg = None):
            """ return [] if all mandatory keys found, otherwise return the lost keys """
            if subpkg:
                mkeys = list(SUB_MAND_KEYS)
            else:
                mkeys = list(MAND_KEYS)

            for key in metadata:
                if key in mkeys:
                    mkeys.remove(key)
                    if not mkeys: break

            return mkeys

        def _check_invalid_keys(metadata, subpkg = None):
            """ return list of invalid keys """
            all_keys = list(LIST_KEYS + STR_KEYS + BOOL_KEYS + ('Date', 'MyVersion'))
            if not subpkg:
                all_keys.append('SubPackages')

            keys = []
            for key in metadata:
                if key not in all_keys:
                    keys.append(key)

            return keys

        def _check_group(metadata):
            if metadata.has_key("Group"):
                warn = True
                for line in open("/usr/share/spectacle/GROUPS"):
                    if metadata['Group'] in line:
                        warn = False
                        break
                if warn:
                    logger.warning('Group \'%s\' is not in the list of approved groups. See /usr/share/spectacle/GROUPS for the complete list.' % (metadata['Group']))

        def _check_pkgconfig():
            pkgcfg = csv.reader(open('/usr/share/spectacle/pkgconfig-provides.csv'), delimiter=',')
            for row in pkgcfg:
                pc = re.search('pkgconfig\(([^)]+)\)', row[1])
                m = pc.group(1)
                if self.packages.has_key(row[0]):
                    ll = self.packages[row[0]] 
                    ll.append(m)
                    self.packages[row[0]] = ll
                else:
                    self.packages[row[0]] = [m]

        def _check_desc(metadata):
            """ sub-routine for 'description' checking """
            if 'Description' not in metadata or \
                metadata['Description'] == '%{summary}':
                return False
            return True

        def _check_listkey(metadata, key):
            """ sub-routine for LIST typed keys checking """
            if key in metadata and not isinstance(metadata[key], list):
                return False
            return True

        def _check_strkey(metadata, key):
            """ sub-routine for STR typed keys checking """
            if key in metadata and not isinstance(metadata[key], str):
                return False
            return True

        def _check_boolkey(metadata, key):
            """ sub-routine for boolean typed keys checking """
            if key in metadata and not isinstance(metadata[key], bool):
                return False
            return True

        def _check_localename(metadata):
            """ sub-routine for 'LocaleName' checking """
            if 'LocaleOptions' in metadata and 'LocaleName' not in metadata:
                return False
            return True

        # checking for mandatory keys
        keys = _check_mandatory_keys(self.metadata)
        if keys:
            logger.error('Missing mandatory keys for main package: %s' % ', '.join(keys))
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                keys = _check_mandatory_keys(sp, sp['Name'])
                if keys:
                    logger.error('Missing mandatory keys for sub-pkg %s: %s' % (sp['Name'], ', '.join(keys)))

        # checking for unexpected keys
        keys = _check_invalid_keys(self.metadata)
        if keys:
            logger.warning('Unexpected keys found: %s' % ', '.join(keys))
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                keys = _check_invalid_keys(sp, sp['Name'])
                if keys:
                    logger.warning('Unexpected keys for sub-pkg %s found: %s' % (sp['Name'], ', '.join(keys)))


        if self.metadata.has_key("PkgBR"):
            _check_pkgconfig()
            pcbr = []
            br = []
            for p in self.metadata['PkgBR']:
                px = p.split(" ")[0]
                px = px.strip()
                pl = self.packages
                if pl.has_key(px):
                    if len(pl[px]) == 1:
                        pcbr.append(pl[px][0])
                    logger.warning("""Please use one of the followings:
           - %s
         in PkgConfigBR instead of %s in PkgBR""" %('\n           - '.join(pl[px]), px))
                else:
                    br.append(p)
            
            if len(pcbr) > 0:
                if self.metadata.has_key('PkgConfigBR'):
                    pcbr.extend(self.metadata['PkgConfigBR'])
                print """
Proposal (multiple values skipped, please insert them manually):
PkgConfigBR: 
    - %s
PkgBR:
    - %s
                    """ %('\n    - '.join(pcbr), '\n    - '.join(br))

        # checking for meego valid groups
        _check_group(self.metadata)
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                _check_group(sp)

        # checking for validation of 'Description'
        if not _check_desc(self.metadata):
            logger.warning('main package has no qualified "Description" tag')
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                if not _check_desc(sp):
                    logger.warning('sub-pkg: %s has no qualified "Description" tag' % sp['Name'])

        # checking for validation of 'LocaleName' and 'LocaleOptions'
        if not _check_localename(self.metadata):
            self.metadata['LocaleName'] = "%{name}"
            logger.warning('lost "LocaleName" keyword, use "%{name}" as default')

        # checking for LIST expected keys
        for key in LIST_KEYS:
            if not _check_listkey(self.metadata, key):
                logger.warning('the value of "%s" in main package is expected as list typed' % key)
                self.metadata[key] = [self.metadata[key]]
            if "SubPackages" in self.metadata:
                for sp in self.metadata["SubPackages"]:
                    if not _check_listkey(sp, key):
                        logger.warning('the value of "%s" in %s sub-package is expected as list typed' % (key, sp['Name']))
                        sp[key] = [sp[key]]

        # checking for STR expected keys
        for key in STR_KEYS:
            if not _check_strkey(self.metadata, key):
                logger.warning('the value of "%s" in main package is expected as string typed' % key)
                self.metadata[key] = ' '.join(self.metadata[key])
            if "SubPackages" in self.metadata:
                for sp in self.metadata["SubPackages"]:
                    if not _check_strkey(sp, key):
                        logger.warning('the value of "%s" in %s sub-package is expected as string typed' % (key, sp['Name']))
                        sp[key] = ' '.join(sp[key])

        # checking for BOOL expected keys
        for key in BOOL_KEYS:
            if not _check_boolkey(self.metadata, key):
                logger.warning('the value of "%s" in main package is expected as bool typed, dropped!' % key)
                # just drop it
                del self.metadata[key]
            if "SubPackages" in self.metadata:
                for sp in self.metadata["SubPackages"]:
                    if not _check_boolkey(sp, key):
                        logger.warning('the value of "%s" in %s sub-package is expected as bool typed, dropped!' % (key, sp['Name']))
                        del sp[key]

    def __get_scm_latest_release(self):

        if "Archive" in self.metadata:
            archive = self.metadata['Archive']
            if archive not in ('bzip2', 'gzip'):
                archive = 'bzip2'
        else:
            archive = 'bzip2'

        if archive == 'bzip2':
            appendix = 'bz2'
        else:
            appendix = 'gz'

        scm_url = self.metadata['SCM']

        scm = GitAccess(scm_url)
        logger.info("Getting tags from SCM...")
        top = scm.get_toptag()
        if top and top != self.version:
            logger.warning('Version in YAML shoud be updated according SCM tags')
            self.version = top
            self.metadata['Version'] = self.version

            pwd = os.getcwd()
            if os.path.exists("%s/%s-%s.tar.%s" %(pwd, self.pkg, self.version, appendix )):
                logger.info("Archive already exists, will not creating a new one")
            else:
                logger.info("Creating archive %s/%s-%s.tar.%s ..." % (pwd, self.pkg, self.version, appendix))
                tmp = tempfile.mkdtemp()
                os.chdir(tmp)
                os.system('git clone %s' % scm_url)
                os.chdir( "%s/%s" %(tmp, self.pkg))
                os.system(' git archive --format=tar --prefix=%s-%s/ %s | %s  > %s/%s-%s.tar.%s' \
                        % (self.pkg,
                           self.version,
                           self.version,
                           archive,
                           pwd,
                           self.pkg,
                           self.version,
                           appendix ))
                shutil.rmtree(tmp)

            os.chdir(pwd)

    def __download_sources(self):
        pkg = self.pkg
        rev = self.version
        sources = self.metadata['Sources']

        for s in sources:
            if s.startswith('http://') or s.startswith('https://') or s.startswith('ftp://'):
                target = s.replace('%{name}', pkg)
                target = target.replace('%{version}', rev)
                f_name = os.path.basename(target)
                if not os.path.isfile(f_name):
                    repl = logger.ask('Need to download source package: %s ?(Y/n) ' % f_name)
                    if repl == 'n': break

                    logger.info('Downloading latest source package from: %s' % target)
                    import urlgrabber
                    from urlgrabber.progress import text_progress_meter
                    try:
                        urlgrabber.urlgrab(target, f_name, progress_obj = text_progress_meter())
                    except urlgrabber.grabber.URLGrabError, e:
                        if e.errno == 14: # HTTPError
                            logger.warning('Invalid source URL')
                        else:
                            raise e
                    except KeyboardInterrupt:
                        logger.info('Downloading is interrupted by ^C')
                    """
                    for ext in ('.md5', '.gpg', '.sig', '.sha1sum'):
                        urllib.urlretrieve(target + ext, f_name + ext)
                    """


    def analyze_source(self):
        tarball = None
        for uri in self.metadata['Sources']:
            fpath = os.path.basename(uri)
            fpath = fpath.replace('%{name}', self.pkg)
            fpath = fpath.replace('%{version}', self.version)
            if os.path.exists(fpath):
                try:
                    if tarfile.is_tarfile(fpath):
                        tarball = fpath
                        break
                except:
                    logger.warning('Corrupt tarball %s found!' % fpath)
                    pass

        def pc_files(members):
            for tarinfo in members:
                f = os.path.split(tarinfo.name)[1]
                xx = f.split(".pc.")
                if len(xx) > 1 and xx[1] == "in":
                    extractfile
                    buf = tarinfo.tobuf()
                    print buf

        prefix = None
        if tarball:
            tf = tarfile.open(tarball, 'r:*')
            for member in tf.getmembers():
                if member.type == tarfile.DIRTYPE:
                    prefix = member.name.rstrip('/')
                    break
            
            #analyze_path = tempfile.mkdtemp(dir=os.getcwd(), prefix=".spectacle_")
            #tf.extractll(path=analyze_path, members=pc_files(tf))
            for member in tf.getmembers():
                f = os.path.split(member.name)[1]
                xx = f.split(".pc.")
                if len(xx) > 1 and xx[1] == "in":
                    pc = tf.extractfile(member)
                    # TODO
            tf.close()


        # confirm 'SourcePrefix' is valid
        if 'SourcePrefix' not in self.metadata and 'NoSetup' not in self.metadata:
            # setting the default value firstly
            self.metadata['SourcePrefix'] = '%{name}-%{version}'
            if not prefix or prefix == '.':
                if tarball:
                    prefix, ignore = os.path.basename(tarball).split('.tar.')

            if prefix and prefix != '%s-%s' % (self.pkg, self.version):
                prefix = prefix.replace(self.pkg, '%{name}')
                prefix = prefix.replace(self.version, '%{version}')
                self.metadata['SourcePrefix'] = prefix

    def __parse_series(self, patches, comments):
        comment = ""
        for line in file(SERIES_PATH):
            if not line.strip():
                continue
            if line.startswith('#'):
                comment += line
            else:
                line = line.strip()
                patches.append(line)
                comments.append(comment + '# ' + line)
                comment = ''

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

        # loading data from YAML
        self.metadata.update(yaml.load(self.stream))

        # verifying the sanity
        self.sanity_check()

        # for convenience
        self.pkg = self.metadata['Name']
        self.version = self.metadata['Version']
        self.release = self.metadata['Release']

        self.specfile = "%s.spec" % self.pkg
        self.newspec = True

        # handling 'ExtraSources', extra separated files which need to be install
        # specific paths
        if "ExtraSources" in self.metadata:
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

        # update to SCM latest release
        if "SCM" in self.metadata:
            self.__get_scm_latest_release()

        # if no srcpkg with yaml.version exists in cwd, trying to download
        self.__download_sources()

        # handle patches with extra options
        if "Patches" in self.metadata:
            patches = self.metadata['Patches']

            self.metadata['Patches']   = []
            self.metadata['PatchOpts'] = []
            self.metadata['PatchCmts'] = []
            for patch in patches:
                self.metadata['PatchCmts'].append('# ' + patch)

                if isinstance(patch, str):
                    self.metadata['Patches'].append(patch)
                    self.metadata['PatchOpts'].append('-p1')
                elif isinstance(patch, dict):
                    self.metadata['Patches'].append(patch.keys()[0])
                    self.metadata['PatchOpts'].append(patch.values()[0])
                elif isinstance(patch, list):
                    self.metadata['Patches'].append(patch[0])
                    self.metadata['PatchOpts'].append(' '.join(patch[1:]))

        # detect 'series.conf' in current dir
        if os.path.exists(SERIES_PATH):
            if "Patches" in self.metadata:
                logger.warning('Both "Patches" tag in yaml and series.conf exists, please use only one.')
            else:
                self.metadata['Patches'] = []
                self.metadata['PatchCmts'] = []
                self.__parse_series(self.metadata['Patches'],
                                    self.metadata['PatchCmts'])

        self.analyze_source()

        # clean up all boolean type options, remove redundant ones
        #   for keys with default value FALSE
        for bopt in ('NeedCheckSection',
                     'SupportOtherDistros',
                     'NoAutoReq',
                     'NoAutoProv',
                    ):
            if bopt in self.metadata and not self.metadata[bopt]:
                del self.metadata[bopt]
        #   for keys with default value TRUE
        for bopt in ('UseAsNeeded',
                    ):
            if bopt in self.metadata and self.metadata[bopt]:
                del self.metadata[bopt]

        # check duplicate default configopts
        dup = '--disable-static'
        if 'ConfigOptions' in self.metadata and dup in self.metadata['ConfigOptions']:
            logger.warning('found duplicate configure options: "%s", please remove it' % dup)
            self.metadata['ConfigOptions'].remove(dup)
            if not self.metadata['ConfigOptions']:
                del self.metadata['ConfigOptions']

        # check duplicate requires for base package
        if "SubPackages" in self.metadata:
            if 'Epoch' in self.metadata:
                autodep = "%{name} = %{epoch}:%{version}-%{release}"
            else:
                autodep = "%{name} = %{version}-%{release}"

            for sp in self.metadata["SubPackages"]:
                if 'Requires' in sp and autodep in sp['Requires']:
                    logger.warning('found duplicate Requires for %s in sub-pkg:%s, please remove it' %(autodep, sp['Name']))
                    sp['Requires'].remove(autodep)
                    if not sp['Requires']:
                        del sp['Requires']

        # initialize extra flags for subpkgs
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                self.extra['subpkgs'][sp['Name']] = copy.deepcopy(self.extra_per_pkg)


        """ NOTE
        we need NOT to do the following checking:
         * whether auto-added Requires(include pre/post/preun/postun) duplicated

        They should be checked by users manually.
        """

    def parse_files(self, files = {}, docs = {}):
        for pkg_name,v in files.iteritems():
            if pkg_name == 'main':
                pkg_extra = self.extra
            else:
                pkg_extra = self.extra['subpkgs'][pkg_name]

            for l in v:
                if re.match('.*\.info\..*', l) or re.match('.*(usr/share/info|%{_infodir}).*info.gz$', l):
                    p1 = re.compile('^%doc\s+(.*)')
                    l1 = p1.sub(r'\1', l)
                    pkg_extra['Infos'].append(l1)
                    pkg_extra['Info'] = True
                if re.match('.*\.desktop$', l):
                    pkg_extra['Desktop'] = True
                if re.match('.*\.a$', l):
                    pkg_extra['Static'] = True
                if re.match('.*etc/rc.d/init.d.*', l) or re.match('.*etc/init.d.*', l):
                    pkg_extra['Service'] = True
                if re.match('.*(%{_libdir}|%{_lib}).*', l) and re.match('.*so.*', l) or \
                   re.match('.*(/ld.so.conf.d/).*', l):
                    if pkg_name != 'devel' and not pkg_name.endswith('-devel'):
                        # 'devel' sub pkgs should not set Lib flags
                        pkg_extra['Lib'] = True
                if re.match('.*(%{_libdir}|%{_lib}).*', l) and re.match('.*\.a$', l):
                    # if *.a found, set 'HasStatic' flag for MAIN pkg
                    self.extra['HasStatic'] = True
                if re.match('.*\.schema.*', l):
                    comp = l.split()
                    if len(comp) > 1:
                        l = comp[1]
                    pkg_extra['Schema'] = True
                    pkg_extra['Schemas'].append(l)
                if re.match('.*\/icons\/.*', l):
                    pkg_extra['Icon'] = True

        # files listed in '%doc' need handling
        for pkg_name,v in docs.iteritems():
            if pkg_name == 'main':
                pkg_extra = self.extra
            else:
                pkg_extra = self.extra['subpkgs'][pkg_name]

            for l in v:
                for item in l.split(' '):
                    if re.match('.*\.info.*', item) or \
                       re.match('.*(usr/share/info|%{_infodir}).*', item):
                        pkg_extra['Info'] = True
                        pkg_extra['Infos'].append(item)

    def parse_existing(self, spec_fpath):
        sin = re.compile("^# >> ([^\s]+)\s*(.*)")
        sout = re.compile("^# << ([^\s]+)\s*(.*)")

        # temp vars
        recording = []
        record = False

        files = {}
        install = {}
        build = {}
        macros = {}         # global macros
        setup = {}
        check_scriptlets = [] # extra headers

        for i in file(spec_fpath).read().split("\n"):
            matchin = sin.match(i)
            matchout = sout.match(i)

            if matchin and not record:
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
                elif matchout.group(1) == "setup":
                    setup['main'] = recording
                elif matchout.group(1) == "check_scriptlets":
                    check_scriptlets = recording

            if record:
                recording.append(i)

        content= { "files" : files,
                   "install": install,
                   "build" : build,
                 }

        if macros:
           content["macros"] = macros
        if setup:
           content["setup"] = setup

        if check_scriptlets and 'NeedCheckSection' in self.metadata:
           content["check_scriptlets"] = check_scriptlets

        # checking whether both 'Files' key and inline files exists
        if files:
            files_yaml = False
            if 'Files' in self.metadata and self.metadata['Files']:
                files_yaml = True
            elif 'SubPackages' in self.metadata:
                for spkg in self.metadata['SubPackages']:
                    if 'Files' in spkg:
                        files_yaml = True
                        break

            if files_yaml:
                logger.warning('both "Files" YAML keyword and inline %file content in spec present')

        # try to remove duplicate '%defattr' in files list
        dup = '%defattr(-,root,root,-)'
        for key in content['files']:
            if dup in content['files'][key]:
                logger.warning('found duplicate "%s" in file list, removed!' % dup)
                content['files'][key].remove(dup)

        return content

    def process(self, extra_content):
        """ Read in old spec and record all customized stuff,
            And auto-detect extra infos from %files list
        """

        # backup old spec file if needed
        if os.path.exists(self.specfile):
            if self.clean_old:
                # backup original file
                backdir = 'spec.backup'
                try:
                    os.mkdir(backdir)
                except:
                    pass
                bak_spec_fpath = os.path.join(backdir, self.specfile)
                if os.path.exists(bak_spec_fpath):
                    repl = logger.ask('%s will be overwritten by the backup, continue?(Y/n) ' % bak_spec_fpath)
                    if repl == 'n':
                        sys.exit(1)

                logger.info('Old spec file is saved as "%s"' % bak_spec_fpath)
                os.rename(self.specfile, bak_spec_fpath)
            else:
                self.newspec = False

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
            docs = {}
            if 'Documents' in self.metadata:
                docs['main'] = self.metadata['Documents']
            if "SubPackages" in self.metadata:
                for sp in self.metadata["SubPackages"]:
                    if 'Documents' in sp:
                        docs[sp['Name']] = sp['Documents']

            # TODO, cleanup docs handling when all pkgs need not, include spec.tmpl
            if docs:
                logger.warning('please move "Docments" values to %files section in .spec!')

            files = copy.deepcopy(self.extra['content']['files'])
            if 'Files' in self.metadata:
                if 'main' in files:
                    files['main'] += self.metadata['Files']
                else:
                    files['main'] = self.metadata['Files']
            if "SubPackages" in self.metadata:
                for sp in self.metadata["SubPackages"]:
                    if 'Files' in sp:
                        if sp['Name'] in files:
                            files[sp['Name']] += sp['Files']
                        else:
                            files[sp['Name']] = sp['Files']

            self.parse_files(files, docs)
        except KeyError:
            pass

        spec_content = str(
                spec.spec(searchList=[{
                                        'metadata': self.metadata,
                                        'extra': self.extra
                                      }]))

        file = open(specfile, "w")
        file.write(spec_content)
        file.close()

def generate_rpm(yaml_fpath, clean_old = False, extra_content = None):
    rpm_writer = RPMWriter(yaml_fpath, clean_old)
    rpm_writer.parse()
    rpm_writer.process(extra_content)

    return rpm_writer.specfile, rpm_writer.newspec
