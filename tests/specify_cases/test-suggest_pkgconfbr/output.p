--- output.orig.spec	2010-03-17 21:15:18.000000000 +0800
+++ output.spec	2010-03-17 21:15:18.000000000 +0800
@@ -14,6 +14,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  libX11-devel
 
 %description
 Sample package for spectacle testings, which will be used as
