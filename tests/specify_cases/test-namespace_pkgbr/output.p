--- output.orig.spec	2010-03-30 17:14:08.000000000 +0800
+++ output.spec	2010-03-30 17:14:42.000000000 +0800
@@ -14,6 +14,13 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  common-br
+%ifarch %{arm}
+BuildRequires:  arm-br
+%endif
+%ifarch %{ix86}
+BuildRequires:  x86-br
+%endif
 
 %description
 Sample package for spectacle testings, which will be used as
