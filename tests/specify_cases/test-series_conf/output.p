--- output.orig.spec	2010-12-09 11:35:07.955977830 +0800
+++ output.spec	2010-12-09 11:35:08.076019664 +0800
@@ -14,6 +14,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Patch0:     patch1.patch
+Patch1:     patch2.patch
 
 
 %description
@@ -35,6 +37,16 @@ This package contains development files
 %prep
 %setup -q -n %{name}-%{version}
 
+# comment of patch1
+# patch1.patch
+# patch1.patch
+%patch0 -p1
+# 
+# comment of patch2
+# patch2.patch
+# patch2.patch
+%patch1 -p1
+# 
 # >> setup
 # << setup
 
