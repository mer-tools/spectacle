# Spectacle Tutorial

## Introduction
Spectacle is the toolset for packaging maintenance of MeeGo, including the tool
to generate spec files from metadata file in YAML format, and tools to convert
spec files or spec-builder's ini files to YAML format.

For spectacle managed packages, all generic packaging information will be stored
in the YAML file, and it also allows maintaining customizations in the spec file
directly with special enclosure tags.

Three separated tools will be installed:

* specify: the tool to generate or to update spec file, based on YAML
* ini2spectacle: the tool to convert spec-builder .ini to YAML and new spec file
* spec2spectacle: the tool to convert original spec to YAML and new spec file

## Installation
### Instruction
Several methods available for spectacle installation:

* rpm/deb packages for several supported Linux distributions

    From [MeeGo Repos](http://repo.meego.com/tools/repo/), repo urls can be found for:

    * MeeGo
    * Fedora 10,11,12
    * openSUSE(s)
    * xUbuntu 8.10/9.04/9.10
    * Debian 5.0

* Download the latest source package, and install it by ``make install``

    (Only running ``setup.py install`` is not enough!)

    The latest code in git tree can be accessed at:
    [git tree](git://gitorious.org/meego-developer-tools/spectacle.git)

### Requirements
* python 2.x, above 2.5
* PyYAML, the python module for YAML parsing
* cheetah, one popular templating system for python
  * In many linux distributions, the package may be named as python-cheetah.

## Usage
### specify
    Usage: specify [options] [yaml-path]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -o OUTFILE_PATH, --output=OUTFILE_PATH
                            Path of output spec file
      -s, --skip-scm        Skip to check upstream SCM when specified in YAML
      -N, --not-download    Do not try to download newer source files
      -n, --non-interactive
                        Non interactive running, to use default answers

### ini2spectacle
    Usage: ini2spectacle [options] [ini-path]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -o OUTFILE_PATH, --output=OUTFILE_PATH
                            Path of output yaml file
      -f, --include-files   To store files list in YAML file

### spec2spectacle
    Usage: spec2spectacle [options] [spec-path]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -o OUTFILE_PATH, --output=OUTFILE_PATH
                            Path of output yaml file
      -r, --replace-macros  To replace self-defined macros in spec file
      --no-builder-parsing  Do NOT try to parse build/install scripts
      -f, --include-files   To store files list in YAML file

## Syntax of spectacle YAML
The syntax of YAML can be refered here: <http://www.yaml.org/spec/>

Two example spectacle YAML files are placed to examples/ directory in source
code:

* xfce4-session.yaml, a real world sample with most of the elements
* general.yaml, a fake spectacle contains all the available elements,
    with comments

All available directives for spectacle are listed as the following:

* Name: **string**

* Summary: **string**

* Version: **string**, version string

* Release: **string**

* Epoch: **string**

* Group: **string**

* License: **string**

* URL: **string**

* SCM: **string**, URL to git tree

* Archive: **string**, format for output of SCM tarball, e.g., gzip, bzip2, xz

* BuildArch: **string**

* ExclusiveArch: **string**

* Prefix: **string**

* LocaleName: **string**

* LocaleOptions: **string**

* Description: **text**

* Sources: **list** of **string**

* SourcePrefix: **string**, specify the prefix path in source package

* ExtraSources: **list** of **string**

* SetupOptions: **string**, the options string for %setup

* Patches: **list** of **string**, all patches need to be in 'p1' level

* Requires: **list** of **string**

* RequiresPre: **list** of **string**

* RequiresPreUn: **list** of **string**

* RequiresPost: **list** of **string**

* RequiresPostUn: **list** of **string**

* PkgBR: **list** of **string**, packages required in building, or BuildRequires

* PkgConfigBR: **list** of **string**, pkg-config requires in building

* Provides: **list** of **string**

* Conflicts: **list** of **string**

* Obsoletes: **list** of **string**

* BuildConflicts: **list** of **string**

* Macros: **list** of **string**

* Macros2: **list** of **string**

* Configure: **string**, valid values: **autogen**, **configure**,
  **reconfigure**, **cmake**, **none**
  **If not specified, the default value "configure" will be used**

* ConfigOptions: **list**, extra options for ``Configure``

* Builder: **string**, valid values: **make**, **single-make**,
  **python**, **python3**, **perl**, **qmake**, **qmake5**, **qtc**, **qtc5**, **cmake**, **none**
  **If not specified, the deault value "make" will be used. If do not want a
  automatic builder, please use "none".**

* QMakeOptions: **list**, extra options for **qmake** ``Builder``

* Files: **list** of **string**, content of ``%files`` for small packages

* FilesInput: **string**, extra input source for %files

* NoFiles: **boolean**, if to be set as True, means no %files section for this package and it cause no rpm generated

* RunFdupes: **string**, path under %buildroot to run ``%fdupes`` macro in %install

* RpmLintIgnore: **list**, list of skip items for ``rpmlint``

* Check: **boolean**, whether need ``%check`` section in spec

* UseAsNeeded: **boolean**, whether export LD\_AS\_NEEDED=1 environ variable before building

* NoAutoReq: **boolean**, whether add 'AutoReq: 0' to spec

* NoAutoProv: **boolean**, whether add 'AutoProv: 0' to spec

* NoSetup: **boolean**, whether to skip using ``%setup`` in ``%prep``

* NoAutoLocale: **boolean**, whether to use ``%find_lang`` to search locale data when found 'intltool' in PkgBR

* NoDesktop: **boolean**, whether to install the desktop files in package

* UpdateDesktopDB: **boolean**, whether to run 'update-desktop-database' to flush cache when package (un)installation

* NoIconCache: **boolean**, whether to run 'gtk-update-icon-cache' if icon files found in package

* AutoDepend: **boolean**, for subpackages only, whether to add Require to main package automatically

* AsWholeName: **boolean**, for subpackages only, whether to use **Name** as the whole package name

* AutoSubPackages: **list** of **string**, mainly for '-devel'

* SubPackages: **list** of **dict**, the **dict** item is the lower level
directives for sub packages:

    * Name
    * Summary
    * Description
    * Group
    * etc.

**CAUTION**: The following cases of value string have special meaning in YAML syntax:

* string with leading **``%``** charactor
* string with leading **``*``** charactor
* string contains **``:``** charactor and one or more spaces/tabs after **``:``**
* string end with **``:``** charactor

**Then these string values need to be quoted by ``'``(single-quote) or ``"``
(double-quote), and the choice of quote char should not conflict with the value
string self.**

## Mandatory and valid keywords for all packages
### Mandatory keywords
The following keywords are mandatory for main package:

* Name
* Summary
* Description
* Version
* Group
* License

The following keywords are mandatory for sub-package:

* Name
* Summary
* Description
* Group

### Valid keywords for sub-packages
For sub-packages, only a subset of keywords can be specified:

* Name
* Summary
* Description
* Group
* License
* Version
* Release
* Epoch
* URL
* BuildArch
* Files
* Prefix
* Requires
* RequiresPre
* RequiresPreUn
* RequiresPost
* RequiresPostUn
* Provides
* Conflicts
* Obsoletes
* NoAutoReq
* NoAutoProv
* NoAutoReqProv
* NoIconCache
* FilesInput

### Keywords only for sub-packages
The following keywords are only valid for sub-packages:

* AsWholeName
* AutoDepend

## Namespace support for multi-architecture in several keywords
For the following spectacle YAML keywords:

* Requires
* PkgBR
* PkgConfigBR
* Patches
* ConfigOptions
* QMakeOptions

If one of the items need to be architecture specified, we can add arch prefix to
it. The supported prefix and the corresponding architectures as the followings:

* ``ix86:`` -   x86 platform
* ``arm:``  -   generic arm platform
* ``armv5:``  -   armv5 platform, will expand to "armv5el armv5tel armv5tejl"
* ``armv7:``  -   armv7 platform, will expand to "armv7el armv7tel armv7l armv7hl armv7nhl"

Here's some samples:

    Requires:
        - arm:pkg-need-in-arm-image
        - ix86:pkg-need-in-x86-image
        - normal-pkg
    ConfigOptions:
        - arm:--arm-specific-opt
        - ix86:--ix86-specific-opt
        - --common-opt

## Customizations in spec
Generated spec files by specify will have many placeholders for customizations,
such as:

    # >> build pre
    # << build pre

You can add any custom code between the markers, next time when you run
``specify``, the text between the markers will be kept as is, all other sections
relying on the meta data from the YAML file will be changed depending on the
values in the YAML file.

The following placeholders in spec can be customized:

* Private Macros, used in this package's spec

    With placeholder:

        # >> macros
        # << macros

* Private Macros2, used in this package's spec

        # >> macros2
        # << macros2

**NOTE**: The placeholder lines will NOT generated in spec by default. If
you need customized macros2, it need be added manually before %pre section
of the .spec file, and only once.

* Extra setup scripts in the last of ``%prep``

    With placeholder:

        # >> setup
        # << setup

* Pre-Build, scripts before package building

    With placeholder:

        # >> build pre
        # << build pre

* Post-Build, scripts after package building

    With placeholder:

        # >> build post
        # << build post

* Pre-Install, scripts before package installation

    With placeholder:

        # >> install pre
        # << install pre

* Post-Install, scripts after package installation

    With placeholder:

        # >> install post
        # << install post

* Files, files list in packaged rpm

    With placeholder:

        # >> files [[-p] sub-package]
        # << files [[-p] sub-package]
**NOTE**: "sub-packge" stands for the name of sub-package, and it is optional.
If no sub-package name specified, it means the files of **main** package.
**NOTE**: If the file list is simple enough, you can use YAML *Files* keyword
instead to record it.

* Scripts for %check section

    With placeholder:

        # >> check
        # << check
**NOTE**: Only if YAML boolean *Check* is specifed as ``yes``, %check with
placeholder lines will be generated in .spec.

* Scriptlets for %pre section

    With placeholder:

        # >> pre
        # << pre
**NOTE**: The placeholder lines will NOT generated in spec by default. If
you need customized %pre scripts, it need be added manually, and only once.

* Scriptlets for %preun section

    With placeholder:

        # >> preun
        # << preun
**NOTE**: The placeholder lines will NOT generated in spec by default. If
you need customized %preun scripts, it need be added manually, and only once.

* Scriptlets for %post section

    With placeholder:

        # >> post
        # << post
**NOTE**: The placeholder lines will NOT generated in spec by default. If
you need customized %post scripts, it need be added manually, and only once.

* Scriptlets for %postun section

    With placeholder:

        # >> postun
        # << postun
**NOTE**: The placeholder lines will NOT generated in spec by default. If
you need customized %postun scripts, it need be added manually, and only once.

## Internal Implementation
Spectacle uses cheetah templates to generate the spec file, based the metadata
from YAML file. But the end users need not tackle it.

## Tips
* If to upgrade the pkg to a newer version, you can just edit the
  version string in spectacle YAML file, and when you run ``specify``, it
  will download the needed files for you automatically.

* For packages with locale data, *LocaleName* is needed. If package
  maintainers cannot confirm whether there are locale files, they can just
  do not use *LocaleName* at first, and whenever "unpackaged files" rpm
  packaging errors encountered, it means *LocaleName* should be added. And
  please do not use it for packages without locale data to keep them clean,
  though it will not block the building and packaging.

* When using spec2spectacle/ini2spectacle to generate spectacle, the following
  problems should be checked:

     * Remove duplicate Requires(include pre/post/preun/postun) which were
       added automatically based on the analysis of file list.
     * Review and clean up the reserved scripts in "build|install pre|post"
       sections in new generated spec file.

* User can use "series.conf" file to specify multiple patches under package directory.
  The "series.conf" can be used by ``quilt`` and the content can be updated to spec
  automatically when running ``specify``.
