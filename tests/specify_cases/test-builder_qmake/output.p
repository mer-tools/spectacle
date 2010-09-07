--- output.orig.spec	2010-06-21 16:39:41.000000000 +0800
+++ output.spec	2010-06-21 16:39:41.000000000 +0800
@@ -42,7 +42,8 @@ This package contains development files 
 # >> build pre
 # << build pre
 
-
+%qmake
+make %{?jobs:-j%jobs}
 
 # >> build post
 # << build post
@@ -50,6 +51,7 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%qmake_install
 
 # >> install post
 # << install post
