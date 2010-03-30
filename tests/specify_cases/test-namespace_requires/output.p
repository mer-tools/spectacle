--- output.orig.spec	2010-03-30 17:12:36.000000000 +0800
+++ output.spec	2010-03-30 17:12:37.000000000 +0800
@@ -14,6 +14,13 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+%ifarch %{arm}
+Requires:   arm-pkgs
+%endif
+%ifarch %{ix86}
+Requires:   x86-pkgs
+%endif
+Requires:   common-pkgs
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -26,6 +33,13 @@ specified, plus with one sub package "de
 Summary:    Development files for %{name}
 Group:      Development/Libraries
 Requires:   %{name} = %{version}-%{release}
+%ifarch %{arm}
+Requires:   arm-pkgs
+%endif
+%ifarch %{ix86}
+Requires:   x86-pkgs
+%endif
+Requires:   common-pkgs
 
 %description devel
 This package contains development files for %{name}.
