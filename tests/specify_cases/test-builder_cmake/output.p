--- output.orig.spec	2012-05-29 18:36:31.785887769 +0300
+++ output.spec	2012-05-29 18:36:32.393890788 +0300
@@ -16,6 +16,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  cmake
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -42,7 +43,8 @@ This package contains development files
 # >> build pre
 # << build pre
 
-
+%cmake . 
+make %{?jobs:-j%jobs}
 
 # >> build post
 # << build post
@@ -51,6 +53,7 @@ This package contains development files
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%make_install
 
 # >> install post
 # << install post
