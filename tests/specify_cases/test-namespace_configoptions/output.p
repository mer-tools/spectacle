--- output.orig.spec	2010-06-21 16:41:36.000000000 +0800
+++ output.spec	2010-06-21 16:41:36.000000000 +0800
@@ -42,7 +42,16 @@ This package contains development files 
 # >> build pre
 # << build pre
 
+%configure --disable-static \
+    --common-opt \
+%ifarch %{arm}
+    --arm-opt \
+%endif
+%ifarch %{ix86}
+    --x86-opt
+%endif
 
+make %{?jobs:-j%jobs}
 
 # >> build post
 # << build post
@@ -50,6 +59,7 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%make_install 
 
 # >> install post
 # << install post
