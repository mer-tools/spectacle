--- output.orig.spec	2010-03-30 17:16:00.000000000 +0800
+++ output.spec	2010-03-30 17:16:50.000000000 +0800
@@ -41,7 +41,16 @@ This package contains development files 
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
@@ -49,6 +58,7 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%make_install
 
 # >> install post
 # << install post
