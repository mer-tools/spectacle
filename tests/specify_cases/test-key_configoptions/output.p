--- output.orig.spec	2010-09-17 10:57:05.335249886 +0800
+++ output.spec	2010-09-17 10:57:35.262208389 +0800
@@ -42,7 +42,11 @@ This package contains development files
 # >> build pre
 # << build pre
 
+%configure --disable-static \
+    --yes-one \
+    --no-two
 
+make %{?_smp_mflags}
 
 # >> build post
 # << build post
@@ -50,6 +54,7 @@ This package contains development files
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%make_install
 
 # >> install post
 # << install post
