--- output.orig.spec	2010-12-09 11:34:14.525023916 +0800
+++ output.spec	2010-12-09 11:34:14.645023854 +0800
@@ -14,6 +14,12 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+%ifarch ppc
+Requires:   ppc-pkg
+%endif
+%ifarch sparc
+BuildRequires:  sparc-pkg-devel
+%endif
 
 
 %description
