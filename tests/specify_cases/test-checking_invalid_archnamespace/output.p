--- output.orig.spec	2010-03-30 17:17:41.000000000 +0800
+++ output.spec	2010-03-30 17:18:28.000000000 +0800
@@ -14,6 +14,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires:   ppc:ppc-pkg
+BuildRequires:  sparc:sparc-pkg-devel
 
 %description
 Sample package for spectacle testings, which will be used as
