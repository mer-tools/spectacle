--- output.orig.spec	2011-02-22 11:14:58.314960674 +0800
+++ output.spec	2011-02-22 11:14:58.433960720 +0800
@@ -14,6 +14,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  libX11-devel
 
 
 %description
