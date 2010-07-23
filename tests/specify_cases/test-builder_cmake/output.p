--- output.orig.spec	2010-07-23 11:15:58.432688797 +0800
+++ output.spec	2010-07-23 11:16:29.632109944 +0800
@@ -42,7 +42,10 @@ This package contains development files 
 # >> build pre
 # << build pre
 
-
+mkdir meego-build
+cd meego-build
+cmake .. 
+make %{?jobs:-j%jobs}
 
 # >> build post
 # << build post
@@ -50,6 +53,8 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+cd meego-build
+%make_install 
 
 # >> install post
 # << install post
