--- output.orig.spec	2010-09-17 10:57:44.102208294 +0800
+++ output.spec	2010-09-17 10:58:15.364208593 +0800
@@ -42,7 +42,11 @@ This package contains development files
 # >> build pre
 # << build pre
 
+%qmake  \
+    --qmake-one \
+    --qmake-two
 
+make %{?_smp_mflags}
 
 # >> build post
 # << build post
@@ -50,6 +54,7 @@ This package contains development files
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%qmake_install
 
 # >> install post
 # << install post
