--- output.orig.spec	2012-07-02 15:35:03.231573645 +0300
+++ output.spec	2012-07-02 15:35:03.346573648 +0300
@@ -16,6 +16,12 @@ License:    BSD
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
 Sample package for spectacle testings, which will be used as
