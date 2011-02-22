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
import datetime
import csv
import tarfile

# third-party modules
import yaml

# internal modules
import __version__
import spec
import logger
from vercmp import FairVersion as _V

SERIES_PATH = 'series.conf'

MAND_KEYS = ('Name',
             'Summary',
             'Description',
             'Version',
             'Group',
             'License',
            )

SUB_MAND_KEYS = ('Name',
                 'Summary',
                 'Description',
                 'Group',
                )

# boolean keys with the default 'False' value
BOOLNO_KEYS = ('Check',
               'SupportOtherDistros',
               'NoAutoReq',
               'NoAutoProv',
               'NoAutoReqProv',
               'NoSetup',
               'NoAutoLocale',
               'AsWholeName',
               'NoFiles',
               'NoDesktop',
               'UpdateDesktopDB',
               'NoIconCache',
              )
# boolean keys with the default 'True' value
BOOLYES_KEYS = ('UseAsNeeded',
                'AutoDepend',
               )
BOOL_KEYS = BOOLNO_KEYS + BOOLYES_KEYS

LIST_KEYS = ('Sources',
             'ExtraSources',
             'Patches',
             'ConfigOptions',
             'QMakeOptions',
             'Requires',
             'RequiresPre',
             'RequiresPreUn',
             'RequiresPost',
             'RequiresPostUn',
             'PkgBR',
             'PkgConfigBR',
             'Provides',
             'Conflicts',
             'BuildConflicts',
             'Obsoletes',
             'AutoSubPackages',
             'Files',
             'Documents',
             'RunFdupes',
             'RpmLintIgnore'
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
             'SCM',
             'Archive',
             'BuildArch',
             'ExclusiveArch',
             'SourcePrefix',
             'Configure',
             'Builder',
             'SetupOptions',
             'LocaleName',
             'LocaleOptions',
             'FilesInput',
             'PostScripts',
             'Prefix',
            )

SUBONLY_KEYS = ('AsWholeName',
                'AutoDepend',
                )

SUBWARN_KEYS = ('PkgBR',
                'PkgConfigBR',
                'BuildConflicts',
               )
SUBAVAIL_KEYS = ('Name',
                 'Summary',
                 'Description',
                 'Group',
                 'License',
                 'Files',
                 'Prefix',
                 'Requires',
                 'RequiresPre',
                 'RequiresPreUn',
                 'RequiresPost',
                 'RequiresPostUn',
                 'Provides',
                 'Conflicts',
                 'Obsoletes',
                 'NoAutoReq',
                 'NoAutoProv',
                 'NoAutoReqProv',
                 'NoIconCache',
                 'FilesInput',
                 'Version', 'Release', 'Epoch', 'URL', 'BuildArch' # very rare
                )

DROP_KEYS = ('PostScripts',
             'Documents',
            )

RENAMED_KEYS = {'NeedCheckSection': 'Check',
                'NoLocale': 'NoAutoLocale',
               }

TYPO_KEYS = {'BuildRequires': 'PkgBR or PkgConfigBR',
             'Url': 'URL',
            }

ARCHED_KEYS = ('Requires',
               'PkgBR',
               'PkgConfigBR',
               'Patches',
               'ConfigOptions',
               'QMakeOptions',
              )
ARCHS = {'ix86': '%{ix86}',
         'arm': '%{arm}',
         'armv5': 'armv5el armv5tel armv5tejl',
         'armv7': 'armv7el armv7tel armv7l armv7hl armv7nhl',
        }

CONFIGURES = ('configure', 'reconfigure', 'autogen', 'cmake', 'none')
BUILDERS = ('make', 'single-make', 'python', 'perl', 'qmake', 'cmake', 'none')

# global helper functions
def arch_split(value):
    m = re.match('^(\w+):([^:]+)', value)
    if m:
        arch = m.group(1)
        left = m.group(2)
        if arch in ARCHS:
            return arch, ARCHS[arch], left
        else:
            return arch, arch, left

    else:
        return '', '', value

class GitAccess():
    def __init__(self, path):
        self.path = path

    def _gettags(self):
        tags = {}
        try:
            fh = os.popen('git ls-remote --tags "%s" 2>/dev/null' % self.path)

            prefix = 'refs/tags/'
            for line in fh:
                line = line.strip()
                node, tag = line.split(None, 1)
                if not tag.startswith(prefix):
                    continue
                tagx = tag[len(prefix):len(tag)]
                tags[tagx] = node
        except KeyboardInterrupt:
            sys.exit(2)

        return tags

    def get_toptag(self):
        vers = [_V(tag) for tag in self._gettags()]
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
                        'DesktopDB': False,
                        'Schema': False,
                        'Schemas': [],
                        'Lib': False,
                        'HasStatic': False,
                        'Icon': False,
                        'Service': False,
                        'Info': False,
                        'Infos': [],
                    }

    def __init__(self, yaml_fpath, spec_fpath=None, clean_old=False, download_new=True, skip_scm=False):
        self.yaml_fpath = yaml_fpath
        now = datetime.datetime.now()
        self.metadata = {'MyVersion': __version__.VERSION, 'Date': now.strftime("%Y-%m-%d")}
        self.pkg = None
        self.version = None
        self.release = None
        self.specfile = spec_fpath
        self.packages = {}

        self.clean_old = clean_old
        self.download_new = download_new
        self.skip_scm = skip_scm
        self.uiwidget = None # default as gtk2 if Qt not detected

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
        # debugging
        import pprint
        pprint.pprint(yaml.dump(yaml.load(self.stream)))

    def _check_dup_files(self, files):
        # try to remove duplicate '%defattr' in files list
        dup1 = '%defattr(-,root,root,-)'
        dup2 = '%defattr(-,root,root)'
        found_dup = dup1 if dup1 in files else dup2 if dup2 in files else None
        if found_dup:
            logger.warning('found duplicate "%s" in file list, removed!' % found_dup)
            files.remove(found_dup)

    def _check_dup_ldconfig(self, pkgname = None):
        if not pkgname:
            pkgname = 'main'
            if not self.extra['Lib']:
                return
        else:
            if not self.extra['subpkgs'][pkgname]['Lib']:
                return

        dup1 = '/sbin/ldconfig'
        dup2 = 'ldconfig'

        for sec in ('post', 'postun'):
            try:
                extra = self.extra['content'][sec][pkgname]
            except KeyError:
                continue
            found_dup = dup1 if dup1 in extra else dup2 if dup2 in extra else None
            if found_dup:
                extra.remove(found_dup)
                logger.warning('Found duplicate "%s" calling in "%%%s" of %s package, removed!' % (found_dup, sec, pkgname))

    def _check_dup_scriptlets(self, pkgname = None):
        if not pkgname:
            pkgname = 'main'
            extra = self.extra
        else:
            extra = self.extra['subpkgs'][pkgname]

        if extra['Desktop']:
            re_idstr = re.compile('^desktop-file-install\s+')
            try:
                lines = extra['content']['install']['pre'] + \
                        extra['content']['install']['post']
            except KeyError:
                pass
            else:
                for line in lines:
                    if re_idstr.match(line):
                        logger.warning('Found possible duplicate "desktop-file-install" script in post install')
                        break

            if extra['DesktopDB']:
                re_idstr = re.compile('^update-desktop-database\s+')
                for sec in ('post', 'postun'):
                    try:
                        lines = self.extra['content'][sec][pkgname]
                    except KeyError:
                        continue

                    for line in lines:
                        if re_idstr.match(line):
                            logger.warning('Found possible duplicate "update-desktop-database" script in %%%s of %s package'%(sec, pkgname))
                            break

        if extra['Info']:
            re_idstr = re.compile('^%install_info')
            for sec in ('post', 'postun'):
                try:
                    lines = self.extra['content'][sec][pkgname]
                except KeyError:
                    continue

                for line in lines:
                    if re_idstr.match(line):
                        logger.warning('Found possible duplicate "%%install_info..." script in %%%s of %s package'%(sec, pkgname))
                        break

        if extra['Icon']:
            re_idstr = re.compile('^/bin/touch\s+.*%{_datadir}/icons/hicolor.*')
            re_idstr2 = re.compile('gtk-update-icon-cache\s+')
            for sec in ('post', 'postun'):
                try:
                    lines = self.extra['content'][sec][pkgname]
                except KeyError:
                    continue

                for line in lines:
                    if re_idstr.match(line):
                        logger.warning('Found possible duplicate script to touch icons in %%%s of %s package'%(sec, pkgname))
                    elif re_idstr2.search(line):
                        logger.warning('Found possible duplicate "gtk-update-icon-cache" script in %%%s of %s package'%(sec, pkgname))

        if extra['Schema']:
            re_idstr = re.compile('gconftool-2\s+')
            for sec in ('post', 'pre', 'preun'):
                try:
                    lines = self.extra['content'][sec][pkgname]
                except KeyError:
                    continue

                for line in lines:
                    if re_idstr.search(line):
                        logger.warning('Found possible duplicate "gconftool-2" script in %%%s of %s package'%(sec, pkgname))
                        break

    def sanity_check(self):

        def _check_empty_keys(metadata):
            """ return the empty keys """
            keys = []
            for key in metadata.keys():
                if metadata[key] is None:
                    keys.append(key)
                    del metadata[key]

            return keys

        def _check_mandatory_keys(metadata, subpkg = False):
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
            if not subpkg:
                # main package
                all_keys = list(LIST_KEYS + STR_KEYS + BOOL_KEYS + ('Date', 'MyVersion'))
                all_keys += RENAMED_KEYS.keys()
                all_keys.append('SubPackages')
                for key in SUBONLY_KEYS:
                    all_keys.remove(key)
            else:
                # sub package
                all_keys = list(SUBAVAIL_KEYS + SUBWARN_KEYS + SUBONLY_KEYS)

            keys = []
            for key in metadata:
                if key not in all_keys:
                    keys.append(key)

            # whether the invalid keys are common typo
            for key in keys[:]:
                if key in TYPO_KEYS:
                    logger.warning('"%s" might be a typo of %s, please correct it' %(key,TYPO_KEYS[key]))
                    keys.remove(key)

            return keys

        def _check_subwarn_keys(metadata, subpkg):
            for key in SUBWARN_KEYS:
                if key in metadata:
                    logger.warning('"%s" found in sub-pkg: %s, please consider to move it to main package' %(key, subpkg))

        def _check_key_group(metadata):
            if metadata.has_key("Group"):
                warn = True
                try:
                    for line in open("/usr/share/spectacle/GROUPS"):
                        if metadata['Group'] in line:
                            warn = False
                            break
                except IOError:
                    logger.error('Cannot open "/usr/share/spectacle/GROUPS", maybe the pkg was not installed correctly.')

                if warn:
                    logger.warning('Group \'%s\' is not in the list of approved groups. See /usr/share/spectacle/GROUPS for the complete list.' % (metadata['Group']))

        def _check_key_license(metadata):
            # warning for gplv3
            gpl3_re = re.compile('L?GPL\s*v3', re.I)
            if metadata.has_key("License"):
                if gpl3_re.search(metadata['License']):
                    logger.warning('GPLv3 related license might be unacceptable.')

        def _check_key_epoch(metadata):
            if 'Epoch' in metadata:
                logger.warning('Please consider to remove "Epoch"')

        def _check_pkgconfig():
            try:
                pkgcfg = csv.reader(open('/usr/share/spectacle/pkgconfig-provides.csv'), delimiter=',')
            except IOError:
                logger.error('Cannot open "/usr/share/spectacle/pkgconfig-provides.csv", maybe the pkg was not installed correctly.')

            for row in pkgcfg:
                pc = re.search('pkgconfig\(([^)]+)\)', row[1])
                m = pc.group(1)
                if self.packages.has_key(row[0]):
                    ll = self.packages[row[0]]
                    ll.append(m)
                    self.packages[row[0]] = ll
                else:
                    self.packages[row[0]] = [m]

        def _check_key_desc(metadata):
            """ sub-routine for 'description' checking """
            if metadata['Description'] == '%{summary}' or \
               metadata['Description'] == metadata['Summary']:
                return False
            return True

        def _check_listkey(metadata, key):
            """ sub-routine for LIST typed keys checking """
            if key in metadata and not isinstance(metadata[key], list):
                return False
            return True

        def _check_strkey(metadata, key):
            """ sub-routine for STR typed keys checking """
            if key in metadata and not isinstance(metadata[key], str) and not isinstance(metadata[key], unicode):
                return False
            return True

        def _check_boolkey(metadata, key):
            """ sub-routine for boolean typed keys checking """
            if key in metadata and not isinstance(metadata[key], bool):
                return False
            return True

        def _check_arched_keys(metadata):
            """ sub-routine for ARCH namespace available keys """
            def _check_arch(key, item):
                if isinstance(item, dict):
                    logger.warning('For arch prefixed %s value "%s", please do NOT leave extra spaces after ":", skipped!' % \
                                    (key, ':'.join(map(str, item.popitem()))))
                    return False

                arch = arch_split(item)[0]
                if arch and arch not in ARCHS:
                    logger.warning('unsupport arch namespace: %s in key %s' % (arch, key))

                return True

            for key in ARCHED_KEYS:
                if key in metadata:
                    if key in STR_KEYS:
                        if not _check_arch(key, metadata[key]):
                            del metadata[key]
                    elif key in LIST_KEYS:
                        for item in metadata[key]:
                            if not _check_arch(key, item):
                                metadata[key].remove(item)
                                if not metadata[key]:
                                    del metadata[key]

        def _check_key_localename(metadata):
            """ sub-routine for 'LocaleName' checking """
            if 'LocaleOptions' in metadata and 'LocaleName' not in metadata:
                return False
            return True

        def _check_dropped_keys(metadata):
            for key in DROP_KEYS:
                if key in metadata:
                    logger.warning('Deprecated key: %s found, please use other valid keys' % key)

        def _check_renamed_keys(metadata):
            for key in RENAMED_KEYS:
                if key in metadata:
                    metadata[RENAMED_KEYS[key]] = metadata[key]
                    del metadata[key]
                    logger.warning('Renamed key: %s found, please use %s instead' % (key, RENAMED_KEYS[key]))

        def _check_key_setups(metadata):
            if 'NoSetup' in metadata:
                if 'SetupOptions' in metadata:
                    logger.warning('"SetupOptions" will have NO effect when "NoSetup" specified in YAML')
                if 'SourcePrefix' in metadata:
                    logger.warning('"SourcePrefix" will have NO effect when "NoSetup" specified in YAML')
            else:
                if 'SetupOptions' in metadata and 'SourcePrefix' in metadata:
                    logger.warning('"SourcePrefix" will have NO effect when "SetupOptions" specified in YAML')

        def _check_key_nofiles(metadata):
            if 'Files' in metadata:
                logger.error('both "NoFiles" and "Files" exists in YAML, please correct it')
            for req in ('Requires',
                        'RequiresPre',
                        'RequiresPreUn',
                        'RequiresPost',
                        'RequiresPostUn',
                        'Provides',
                        'Conflicts',
                        'BuildConflicts',
                        'Obsoletes'):
                if req in metadata and metadata[req]:
                    logger.warning('"NoFiles" exists, key %s has no effect any more' % req)

        def _check_key_configure(metadata):
            cfg = metadata['Configure']
            if cfg not in CONFIGURES:
                logger.warning('"%s" is not a valid choice of Configure(%s)' % (cfg, '/'.join(CONFIGURES)))

        def _check_key_builder(metadata):
            builder = metadata['Builder']
            if builder not in BUILDERS:
                logger.warning('"%s" is not a valid choice of Builder(%s)' % (builder, '/'.join(BUILDERS)))
            # checking invalid 'Configure' for special builder
            if builder in ('python', 'perl', 'qmake', 'cmake') and \
               'Configure' in metadata and metadata['Configure'] != 'none':
                logger.warning('"%s" need no "Configure" setting which will be ignored' % builder)

        # checking for empty keys
        keys = _check_empty_keys(self.metadata)
        if keys:
            logger.warning('Please remove empty keys in main package: %s' % ', '.join(keys))
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                keys = _check_empty_keys(sp)
                if keys:
                    logger.warning('Please remove empty keys in %s subpackage: %s' % (sp['Name'], ', '.join(keys)))

        # checking for mandatory keys
        keys = _check_mandatory_keys(self.metadata)
        if keys:
            logger.error('Missing mandatory keys for main package: %s' % ', '.join(keys))
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                keys = _check_mandatory_keys(sp, True)
                if keys:
                    if 'Name' in keys:
                        logger.error('Missing mandatory keys for sub-pkg: Name')
                    else:
                        logger.error('Missing mandatory keys for sub-pkg "%s": %s' % (sp['Name'], ', '.join(keys)))

        # checking for unexpected keys
        keys = _check_invalid_keys(self.metadata)
        if keys:
            logger.warning('Unexpected keys found: %s' % ', '.join(keys))
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                keys = _check_invalid_keys(sp, sp['Name'])
                if keys:
                    logger.warning('Unexpected keys for sub-pkg %s found: %s' % (sp['Name'], ', '.join(keys)))

        # checking for questionable sub-package keys
        if "SubPackages" in self.metadata and 'NoFiles' not in self.metadata:
            for sp in self.metadata["SubPackages"]:
                keys = _check_subwarn_keys(sp, sp['Name'])

        # checking for deprecated keys
        _check_dropped_keys(self.metadata)

        # checking for renamed keys
        _check_renamed_keys(self.metadata)


        ######### Type checkings ##########
        # checking for LIST expected keys
        for key in LIST_KEYS:
            if not _check_listkey(self.metadata, key):
                logger.warning('the value of "%s" in main package is expected as list typed' % key)
                self.metadata[key] = [self.metadata[key]]
            if "SubPackages" in self.metadata:
                for sp in self.metadata["SubPackages"]:
                    if not _check_listkey(sp, key):
                        logger.warning('the value of "%s" in "%s" sub-package is expected as list typed' % (key, sp['Name']))
                        sp[key] = [sp[key]]

        # checking for STR expected keys
        for key in STR_KEYS:
            if not _check_strkey(self.metadata, key):
                logger.warning('the value of "%s" in main package is expected as string typed' % key)
                if isinstance(self.metadata[key], list):
                    self.metadata[key] = ' '.join(self.metadata[key])
                else:
                    del self.metadata[key]
            if "SubPackages" in self.metadata:
                for sp in self.metadata["SubPackages"]:
                    if not _check_strkey(sp, key):
                        logger.warning('the value of "%s" in "%s" sub-package is expected as string typed' % (key, sp['Name']))
                        if isinstance(sp[key], list):
                            sp[key] = ' '.join(sp[key])
                        else:
                            del sp[key]

        # checking for BOOL expected keys
        for key in BOOL_KEYS:
            if not _check_boolkey(self.metadata, key):
                logger.warning('the value of "%s" in main package is expected as bool typed, dropped!' % key)
                # just drop it
                del self.metadata[key]
            if "SubPackages" in self.metadata:
                for sp in self.metadata["SubPackages"]:
                    if not _check_boolkey(sp, key):
                        logger.warning('the value of "%s" in "%s" sub-package is expected as bool typed, dropped!' % (key, sp['Name']))
                        del sp[key]

        ######### checkings for special keys ##########
        # checking for arch namespace enabled keys
        _check_arched_keys(self.metadata)
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                _check_arched_keys(sp)

        # checking for proposal pkgconfig requires
        if self.metadata.has_key("PkgBR"):
            _check_pkgconfig()
            pcbr = []
            br = []
            for p in self.metadata['PkgBR']:
                px = p.split()[0]
                for arch in ARCHS:
                    prefix = arch + ':'
                    if px.startswith(prefix):
                        px = px[len(prefix):]

                pl = self.packages
                if pl.has_key(px):
                    if len(pl[px]) == 1:
                        pcbr.append(pl[px][0])
                    else:
                        br.append(p)
                    logger.warning("""Please use one of the followings:
           - %s
         in PkgConfigBR instead of %s in PkgBR""" %('\n           - '.join(pl[px]), px))
                else:
                    br.append(p)

            if len(pcbr) > 0:
                if self.metadata.has_key('PkgConfigBR'):
                    pcbr.extend(self.metadata['PkgConfigBR'])
                logger.info("""Proposal (multiple values skipped, please insert them manually):
PkgConfigBR:
    - %s
PkgBR:
    - %s
                    """ %('\n    - '.join(pcbr), '\n    - '.join(br)))

        _check_key_epoch(self.metadata)

        # checking for meego valid groups
        _check_key_group(self.metadata)
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                _check_key_group(sp)

        # checking for meego invalid licenses
        _check_key_license(self.metadata)
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                _check_key_license(sp)

        # checking for validation of 'Description'
        if not _check_key_desc(self.metadata):
            logger.error('main package has no qualified "Description" tag')
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                if not _check_key_desc(sp):
                    logger.error('sub-pkg: "%s" has no qualified "Description" tag' % sp['Name'])

        # checking for validation of 'LocaleName' and 'LocaleOptions'
        if not _check_key_localename(self.metadata):
            self.metadata['LocaleName'] = "%{name}"
            logger.warning('lost "LocaleName" keyword, use "%{name}" as default')

        # checking for validation of 'NoSetup', 'SetupOptions' and 'SourcePrefix'
        _check_key_setups(self.metadata)

        # checking for validation of 'NoFiles'
        if 'NoFiles' in self.metadata:
            _check_key_nofiles(self.metadata)

        # checking duplicate 'Files' items
        if 'Files' in self.metadata:
            self._check_dup_files(self.metadata['Files'])
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                if 'Files' in sp:
                    self._check_dup_files(sp['Files'])

        # checking for validation of 'Configure and Builder'
        if 'Configure' in self.metadata:
            _check_key_configure(self.metadata)
        if 'Builder' in self.metadata:
            _check_key_builder(self.metadata)

    def _get_scm_latest_release(self):

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
        if not top or top == self.version:
            # no need to fetch from SCM
            return

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

    def _download_sources(self):
        pkg = self.pkg
        rev = self.version
        sources = self.metadata['Sources']

        for s in sources:
            if s.startswith('http://') or s.startswith('https://') or s.startswith('ftp://'):
                target = s.replace('%{name}', pkg)
                target = target.replace('%{version}', rev)
                f_name = os.path.basename(target)
                if not os.path.isfile(f_name):
                    answer = logger.ask('Need to download source package: %s ?' % f_name)
                    if not answer: break

                    logger.info('Downloading latest source package from: %s' % target)
                    import glob
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
                    else:
                        # After download, asking to remove the possible old tarballs
                        target = s.replace('%{name}', pkg)
                        target = target.replace('%{version}', '*')
                        globname = os.path.basename(target)
                        for f in glob.glob(globname):
                            if f == f_name: continue

                            answer = logger.ask('Possible old source: %s, to delete it?' % f)
                            if not answer: break
                            try:
                                os.remove(f)
                                logger.info('%s Deleted!' % f)
                            except OSError:
                                logger.warning('Cannot delete %s' % f)

    def _analyze_source(self):
        def pc_files(members):
            for tarinfo in members:
                f = os.path.split(tarinfo.name)[1]
                xx = f.split(".pc.")
                if len(xx) > 1 and xx[1] == "in":
                    extractfile
                    buf = tarinfo.tobuf()

        tarball = None
        for uri in self.metadata['Sources']:
            fpath = os.path.basename(uri)
            fpath = fpath.replace('%{name}', self.pkg)
            fpath = fpath.replace('%{version}', self.version)
            if os.path.exists(fpath) and os.path.getsize(fpath):
                try:
                    if tarfile.is_tarfile(fpath):
                        tarball = fpath
                        break
                except:
                    logger.warning('Corrupt tarball %s found!' % fpath)
                    pass

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
                # guess prefix from filename
                if tarball:
                    if '.tar.' in tarball:
                        prefix = os.path.basename(tarball).split('.tar.')[0]
                    else:
                        # strip the ext name
                        prefix = os.path.splitext(tarball)[0]

            if prefix and prefix != '%s-%s' % (self.pkg, self.version):
                prefix = prefix.replace(self.pkg, '%{name}')
                prefix = prefix.replace(self.version, '%{version}')
                self.metadata['SourcePrefix'] = prefix

    def _parse_series(self):
        patches = []
        comments = []

        comment = ''
        for line in file(SERIES_PATH):
            if not line.strip():
                continue
            if line.startswith('#'):
                comment += line
            else:
                line = line.strip()
                patches.append(line)
                comments.append(comment.rstrip())
                comment = ''

        return patches, comments

    def _cleanup_boolkeys(self, items):
        """ clean up all boolean type keys,
            use the exists status to present bool value
        """
        #   for keys with default value FALSE
        for bopt in BOOLNO_KEYS:
            if bopt in items and not items[bopt]:
                del items[bopt]
        #   for keys with default value TRUE
        for bopt in BOOLYES_KEYS:
            if bopt in items and not items[bopt]:
                del items[bopt]
            else:
                items[bopt] = True

    def _gen_auto_requires(self, metadata, extra, pkg_name = 'main'):
        auto_requires = {
                'Lib': {'RequiresPost': ['/sbin/ldconfig'],
                        'RequiresPostUn': ['/sbin/ldconfig'],
                       },
                'Icon': {'RequiresPost': ['/bin/touch', 'gtk2'],
                        },
                'Desktop': {'PkgBR': ['desktop-file-utils'],
                           },
                'DesktopDB': {'RequiresPost': ['desktop-file-utils'],
                              'RequiresPostUn': ['desktop-file-utils'],
                             },
                'Info': {'RequiresPost': ['/sbin/install-info'],
                         'RequiresPostUn': ['/sbin/install-info'],
                        },
                'Service': {'RequiresPost': ['/sbin/service', '/sbin/chkconfig'],
                            'RequiresPostUn': ['/sbin/service', '/sbin/chkconfig'],
                           },
                'Schema': {'RequiresPost': ['GConf2'],
                           'RequiresPreUn': ['GConf2'],
                           'RequiresPre': ['GConf2'],
                          },
        }

        for key,reqs in auto_requires.iteritems():
            if extra[key]:
                for req,items in reqs.iteritems():
                    if req in metadata:
                        for i in items:
                            # e.g. GConf2 >= 0.14
                            yaml_reqs = map(lambda s: s.split()[0], metadata[req])
                            if i in yaml_reqs:
                                if i in metadata[req]:
                                    logger.warning('duplicate item: %s for %s in package %s' % (i,req,pkg_name))
                                # else do nothing
                            else:
                                metadata[req].append(i)
                    else:
                        metadata[req] = items

    def parse(self):

        # customized int/float constructor for Loader of in PyYAML
        # to regard all numbers as plain string
        def _no_number(self, node):
            return str(self.construct_scalar(node))
        yaml.Loader.add_constructor(u'tag:yaml.org,2002:int', _no_number)
        yaml.Loader.add_constructor(u'tag:yaml.org,2002:float', _no_number)

        # loading data from YAML
        try:
            self.metadata.update(yaml.load(self.stream))
        except yaml.scanner.ScannerError, e:
            logger.error('syntax error found in yaml: %s' % str(e))
        except yaml.parser.ParserError, e:
            logger.error('syntax error found in yaml: %s' % str(e))
        except ValueError:
            logger.error('Please check if the input file is in YAML format')
        except TypeError:
            # empty can lead here
            logger.error('Empty yaml file: %s' % self.yaml_fpath)

        # verifying the sanity
        self.sanity_check()

        # for convenience
        self.pkg = self.metadata['Name']
        self.version = self.metadata['Version']
        try:
            self.release = self.metadata['Release']
        except KeyError:
            logger.warning('"Release" not specified, use "1" as the default value')
            self.release = self.metadata['Release'] = '1'

        if not self.specfile:
            self.specfile = "%s.spec" % self.pkg
        self.newspec = True


        if "RpmLintIgnore" in self.metadata:
            rpmlintrc = "%s-rpmlintrc" %self.metadata['Name']
            rpmlint = "from Config import *\n"
            for lint in self.metadata['RpmLintIgnore']:
                rpmlint = rpmlint + "addFilter(\"%s\")\n" %lint

            file = open(rpmlintrc, "w")
            file.write(rpmlint)
            file.close()

        # handling 'ExtraSources', extra separated files which need to be install
        # specific paths
        if "ExtraSources" in self.metadata:

            # confirm 'Sources' valid
            if 'Sources' not in self.metadata:
                self.metadata['Sources'] = []

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

        if self.download_new:
            if not self.skip_scm:
                # update to SCM latest release
                if "SCM" in self.metadata:
                    self._get_scm_latest_release()

            # if no srcpkg with yaml.version exists in cwd, trying to download
            if 'Sources' in self.metadata:
                self._download_sources()

        # handle patches with extra options
        if "Patches" in self.metadata:
            patches = self.metadata['Patches']

            self.metadata['Patches']   = []
            self.metadata['PatchOpts'] = []
            for patch in patches:
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
                self.metadata['Patches'], self.metadata['PatchCmts'] = self._parse_series()

        if 'Sources' in self.metadata:
            self._analyze_source()

        # clean up all boolean type keys, use the exists status to present bool value
        self._cleanup_boolkeys(self.metadata)
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                self._cleanup_boolkeys(sp)

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
                if 'Requires' in sp and autodep in sp['Requires'] and 'AutoDepend' in sp:
                    logger.warning('found duplicate Requires for %s in sub-pkg:%s, please remove it' %(autodep, sp['Name']))
                    sp['Requires'].remove(autodep)
                    if not sp['Requires']:
                        del sp['Requires']

        # initialize extra flags for subpkgs
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                self.extra['subpkgs'][sp['Name']] = copy.deepcopy(self.extra_per_pkg)
        if "AutoSubPackages" in self.metadata:
            for asp in self.metadata["AutoSubPackages"]:
                self.extra['subpkgs'][asp] = copy.deepcopy(self.extra_per_pkg)

        # detect the using UI widget, QT or Gtk2
        all_pkgbr = []
        if 'PkgBR' in self.metadata:
            all_pkgbr += self.metadata['PkgBR']
        if 'PkgConfigBR' in self.metadata:
            all_pkgbr += self.metadata['PkgConfigBR']
        for br in all_pkgbr:
            if br.startswith('Qt'):
                self.uiwidget = 'Qt'

        """ NOTE
        we need NOT to do the following checking:
         * whether auto-added Requires(include pre/post/preun/postun) duplicated

        They should be checked by users manually.
        """

    def _lookup_pkgmeta(self, pkgname):
        if pkgname == 'main':
            return self.metadata

        for sp in self.metadata['SubPackages']:
            if sp['Name'] == pkgname:
                return sp

        # not found
        return {}

    def parse_files(self, files = {}, docs = {}):

        py_path_check = False
        if 'Builder' in self.metadata and self.metadata['Builder'] == 'python':
            py_path_check = True
            if 'BuildArch' in self.metadata and self.metadata['BuildArch'] == 'noarch':
                py_path = '%{python_sitelib}'
            else:
                py_path = '%{python_sitearch}'

        for pkg_name,v in files.iteritems():
            pkg_meta = self._lookup_pkgmeta(pkg_name)

            if pkg_name == 'main':
                pkg_extra = self.extra
            else:
                pkg_extra = self.extra['subpkgs'][pkg_name]

            for l in v:
                if re.match('\s*%exclude\s.*', l):
                    pass # not match anyting excluded files
                elif re.match('.*\.info\..*', l) or re.match('.*(usr/share/info|%{_infodir}).*info\..*$', l):
                    p1 = re.compile('^%doc\s+(.*)')
                    l1 = p1.sub(r'\1', l)
                    pkg_extra['Infos'].append(l1)
                    pkg_extra['Info'] = True
                elif re.match('.*(usr/share|%{_datadir})/applications/.*\.desktop$', l):
                    if 'NoDesktop' not in self.metadata:
                        pkg_extra['Desktop'] = True
                elif re.match('.*(/etc|%{_sysconfdir})/rc.d/init.d/.*', l) or \
                     re.match('.*(/etc|%{_sysconfdir})/init.d/.*', l) or \
                     re.match('.*%{_initddir}/.*', l) or \
                     re.match('.*%{_initrddir}/.*', l):

                    pkg_extra['Service'] = True
                elif re.match('.*(%{_libdir}|%{_lib}|/lib|/usr/lib)/[^/]*[.*?]+so([.*?]+.*$|$)', l) or \
                   re.match('.*(/ld.so.conf.d/).*', l):
                    if pkg_name != 'devel' and not pkg_name.endswith('-devel'):
                        # 'devel' sub pkgs should not set Lib flags
                        pkg_extra['Lib'] = True
                elif re.match('.*(%{_libdir}|%{_lib}).*', l) and re.match('.*\.a$', l):
                    # if *.a found, set 'HasStatic' flag for MAIN pkg
                    self.extra['HasStatic'] = True
                elif re.match('.*\.schema.*', l):
                    comp = l.split()
                    if len(comp) > 1:
                        l = comp[1]
                    pkg_extra['Schema'] = True
                    pkg_extra['Schemas'].append(l)
                elif re.match('.*\/icons\/.*', l):
                    if 'NoIconCache' in pkg_meta and pkg_meta['NoIconCache'] == True:
                        # using "NoIconCache" to avoid cache explicitly
                        continue

                    if self.uiwidget and self.uiwidget == 'Qt':
                        # disable icon files handling for Qt based app
                        continue

                    pkg_extra['Icon'] = True

                # special checking for python packages
                if py_path_check:
                    if '%{python_sitelib}' in l or '%{python_sitearch}' in l:
                        if py_path not in l:
                            logger.error('please use %s in %%files to specify module installation path' % py_path)

        # check whether need to update desktop database
        if 'UpdateDesktopDB' in self.metadata:
            self.extra['DesktopDB'] = True
            if self.extra['Desktop'] != True:
                logger.warning('"UpdateDesktopDB" specified but found no desktop files')

        # files listed in '%doc' need handling
        # TODO to be cleanup
        for pkg_name,v in docs.iteritems():
            if pkg_name == 'main':
                pkg_extra = self.extra
            else:
                pkg_extra = self.extra['subpkgs'][pkg_name]

            for l in v:
                for item in l.split():
                    if re.match('.*\.info.*', item) or \
                       re.match('.*(usr/share/info|%{_infodir}).*', item):
                        pkg_extra['Info'] = True
                        pkg_extra['Infos'].append(item)

    def parse_existing(self, spec_fpath):
        sin = re.compile("^# >> ([^\s]+)\s*(.*)")
        sout = re.compile("^# << ([^\s]+)\s*(.*)")

        version = None

        # temp vars
        recording = []
        record = False

        files = {}
        install = {}
        build = {}
        macros = {}         # global macros
        setup = {}
        pre = {}
        preun = {}
        post = {}
        postun = {}
        check = {} # extra headers

        line_num = 0
        for i in file(spec_fpath):
            i = i.strip()
            if line_num < 3:
                if line_num == 2:
                    m = re.match("^#.*spectacle version (\S+)$", i)
                    if m:
                        version = m.group(1)
                        spec_ver = _V(version)
                        cur_ver = _V(__version__.VERSION)
                        if cur_ver < spec_ver:
                            logger.warning('!!! Current spectacle version is lower than the one used for this package last time')
                            answer = logger.ask('Please upgrade your spectacle firstly, continue?', False)
                            if not answer:
                                sys.exit(1)
                    else:
                        answer = logger.ask('The exist spec file might be not a spectacle generated one, continue?', False)
                        if not answer:
                            sys.exit(1)
                line_num += 1

            matchin = sin.match(i)
            matchout = sout.match(i)

            if matchin and not record:
                record = True
                recording = []
                continue

            if matchout:
                record = False
                if not recording: continue # empty

                if matchout.group(2) and matchout.group(1) in ["files", "post","postun", "pre", "preun"]:
                    if not matchout.group(2) in self.extra['subpkgs']:
                        logger.error('In spec %s section for %s package. Package does not excist in YAML.' % (matchout.group(1), matchout.group(2)))

                if matchout.group(1) == "files":
                    if matchout.group(2):
                        files[matchout.group(2)] = recording
                    else:
                        files['main'] = recording
                elif matchout.group(1) == "post":
                    if matchout.group(2):
                        post[matchout.group(2)] = recording
                    else:
                        post['main'] = recording
                elif matchout.group(1) == "postun":
                    if matchout.group(2):
                        postun[matchout.group(2)] = recording
                    else:
                        postun['main'] = recording
                elif matchout.group(1) == "pre":
                    if matchout.group(2):
                        pre[matchout.group(2)] = recording
                    else:
                        pre['main'] = recording
                elif matchout.group(1) == "preun":
                    if matchout.group(2):
                        preun[matchout.group(2)] = recording
                    else:
                        preun['main'] = recording
                elif matchout.group(1) == "install":
                    install[matchout.group(2)] = recording
                elif matchout.group(1) == "build":
                    build[matchout.group(2)] = recording
                elif matchout.group(1) == "macros":
                    macros['main'] = recording
                elif matchout.group(1) == "setup":
                    setup['main'] = recording
                elif matchout.group(1) == "check" or \
                     matchout.group(1) == "check_scriptlets": #TODO, remove it whenever cleanup
                    check['main'] = recording

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
        if post:
            content["post"] = post
        if postun:
            content["postun"] = postun
        if pre:
            content["pre"] = pre
        if preun:
            content["preun"] = preun

        if check and 'Check' in self.metadata:
            content["check"] = check

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
        for key in content['files']:
            self._check_dup_files(content['files'][key])

        # checking duplicate 'rm -rf %{buildroot}'
        re_cleanup = re.compile('^(?:rm|\%\{__rm\})\W+-rf\W+(?:\$RPM_BUILD_ROOT|\%\{buildroot\})/?$')
        if 'install' in content and 'post' in content['install']:
            if re_cleanup.match(content['install']['post'][0]):
                logger.warning('duplicate buildroot cleanup found in the first line of install_post, remove it')

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
                    answer = logger.ask('%s will be overwritten by the backup, continue?' % bak_spec_fpath)
                    if not answer:
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

        # TODO, cleanup docs handling when all pkgs need not, include spec.tmpl
        docs = {}
        if 'Documents' in self.metadata:
            docs['main'] = self.metadata['Documents']
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                if 'Documents' in sp:
                    docs[sp['Name']] = sp['Documents']

        if 'files' in self.extra['content']:
            files = copy.deepcopy(self.extra['content']['files'])
        else:
            files = {}

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

        # adding automatic requires according %files
        self._gen_auto_requires(self.metadata, self.extra)
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                self._gen_auto_requires(sp, self.extra['subpkgs'][sp['Name']], sp['Name'])

        # check duplicate 'ldconfig' in %post/%postun
        #   actually, all auto generated scripts in %post like sections should be checked
        #   for duplicate issue, but it's not nice to do that according current design.
        #   But for 'ldconfig', there're too many issues with it, the following code
        #   is just a workaround to fix them.
        self._check_dup_ldconfig()
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                self._check_dup_ldconfig(sp['Name'])

        # check duplicate other auto-scriptlets in %post/%postun
        self._check_dup_scriptlets()
        if "SubPackages" in self.metadata:
            for sp in self.metadata["SubPackages"]:
                self._check_dup_scriptlets(sp['Name'])

        spec_content = spec.spec(searchList=[{
                                        'metadata': self.metadata,
                                        'extra': self.extra,
                                        'arch_split': arch_split
                                      }]).respond()

        file = open(specfile, "w")
        file.write(spec_content.encode('utf-8'))
        file.close()

def generate_rpm(yaml_fpath, clean_old = False, extra_content = None, spec_fpath=None, download_new=True, skip_scm=False):
    rpm_writer = RPMWriter(yaml_fpath, spec_fpath, clean_old, download_new, skip_scm)
    rpm_writer.parse()
    rpm_writer.process(extra_content)

    return rpm_writer.specfile, rpm_writer.newspec
