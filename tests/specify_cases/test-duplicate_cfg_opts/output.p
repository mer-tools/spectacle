--- output.orig.spec	2010-06-21 16:41:52.000000000 +0800
+++ output.spec	2010-06-21 16:41:52.000000000 +0800
@@ -42,7 +42,10 @@ This package contains development files 
 # >> build pre
 # << build pre
 
+%configure --disable-static \
+    --otheropt
 
+make %{?jobs:-j%jobs}
 
 # >> build post
 # << build post
@@ -50,6 +53,7 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%make_install 
 
 # >> install post
 # << install post
