--- output.orig.spec	2013-04-10 13:35:16.823402537 +0000
+++ output.spec	2013-04-10 13:35:23.188450600 +0000
@@ -41,7 +41,9 @@ This package contains development files 
 # >> build pre
 # << build pre
 
+%qmake5 
 
+make %{?_smp_mflags}
 
 # >> build post
 # << build post
@@ -50,6 +52,7 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%qmake_install
 
 # >> install post
 # << install post
