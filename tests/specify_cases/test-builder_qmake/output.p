--- output.orig.spec	2010-09-17 10:54:29.816399316 +0800
+++ output.spec	2010-09-17 10:54:32.033206436 +0800
@@ -42,7 +42,9 @@ This package contains development files
 # >> build pre
 # << build pre
 
+%qmake 
 
+make %{?jobs:-j%jobs}
 
 # >> build post
 # << build post
@@ -50,6 +52,7 @@ This package contains development files
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%qmake_install
 
 # >> install post
 # << install post
