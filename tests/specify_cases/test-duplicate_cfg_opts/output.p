--- output.orig.spec	2012-07-02 15:35:07.219573752 +0300
+++ output.spec	2012-07-02 15:35:07.329573755 +0300
@@ -42,7 +42,10 @@ This package contains development files
 # >> build pre
 # << build pre
 
+%configure --disable-static \
+    --otheropt
 
+make %{?_smp_mflags}
 
 # >> build post
 # << build post
@@ -51,6 +54,7 @@ This package contains development files
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%make_install
 
 # >> install post
 # << install post
