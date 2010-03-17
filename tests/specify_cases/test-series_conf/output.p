--- output.orig.spec	2010-03-17 21:15:17.000000000 +0800
+++ output.spec	2010-03-17 21:15:17.000000000 +0800
@@ -14,6 +14,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Patch0:     patch1.patch
+Patch1:     patch2.patch
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -34,6 +36,12 @@ This package contains development files 
 %prep
 %setup -q -n %{name}-%{version}
 
+# comment of patch1
+# patch1.patch
+%patch0 -p1
+# comment of patch2
+# patch2.patch
+%patch1 -p1
 # >> setup
 # << setup
 
