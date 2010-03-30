--- output.orig.spec	2010-03-30 17:14:57.000000000 +0800
+++ output.spec	2010-03-30 17:15:44.000000000 +0800
@@ -14,6 +14,13 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  pkgconfig(common-pkgcfg)
+%ifarch %{arm}
+BuildRequires:  pkgconfig(arm-pkgcfg) >= 0.11
+%endif
+%ifarch %{ix86}
+BuildRequires:  pkgconfig(x86-pkgcfg) >= %{xxx_version}
+%endif
 
 %description
 Sample package for spectacle testings, which will be used as
