--- output.orig.spec	2010-06-21 16:39:53.000000000 +0800
+++ output.spec	2010-06-21 16:39:53.000000000 +0800
@@ -43,6 +43,7 @@ This package contains development files 
 # << build pre
 
 
+make %{?_smp_mflags}
 
 # >> build post
 # << build post
@@ -50,6 +51,7 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%make_install
 
 # >> install post
 # << install post
