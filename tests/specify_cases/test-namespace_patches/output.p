--- output.orig.spec	2010-12-09 13:51:58.537023891 +0800
+++ output.spec	2010-12-09 13:51:58.654023776 +0800
@@ -14,6 +14,13 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Patch0:     common-patch
+%ifarch %{arm}
+Patch1:     arm-only-patch
+%endif
+%ifarch %{ix86}
+Patch2:     x86-only-patch
+%endif
 
 
 %description
@@ -35,6 +42,16 @@ This package contains development files
 %prep
 %setup -q -n %{name}-%{version}
 
+# common-patch
+%patch0 -p1
+%ifarch %{arm}
+# arm-only-patch
+%patch1 -p1
+%endif
+%ifarch %{ix86}
+# x86-only-patch
+%patch2 -p1
+%endif
 # >> setup
 # << setup
 
