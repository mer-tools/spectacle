--- output.orig.spec	2012-07-02 15:35:04.880573689 +0300
+++ output.spec	2012-07-02 15:35:04.996573692 +0300
@@ -16,6 +16,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  libX11-devel
 
 %description
 Sample package for spectacle testings, which will be used as
