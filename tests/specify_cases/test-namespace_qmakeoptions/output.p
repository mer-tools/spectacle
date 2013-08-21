--- output.orig.spec	2013-04-10 13:25:01.662757254 +0000
+++ output.spec	2013-04-10 13:25:01.763758017 +0000
@@ -41,7 +41,16 @@ This package contains development files 
 # >> build pre
 # << build pre
 
+%qmake  \
+%ifarch %{arm}
+    --arm-only \
+%endif
+%ifarch %{ix86}
+    --ix86-only \
+%endif
+    --common-one
 
+make %{?_smp_mflags}
 
 # >> build post
 # << build post
@@ -50,6 +59,7 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%qmake_install
 
 # >> install post
 # << install post
