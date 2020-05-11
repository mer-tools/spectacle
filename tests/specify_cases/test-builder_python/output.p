--- output.orig.spec
+++ output.spec
@@ -41,8 +41,8 @@
 # >> build pre
 # << build pre
 
+%{py3_build}
 
-
 # >> build post
 # << build post
 
@@ -50,6 +50,7 @@
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%{py3_install}
 
 # >> install post
 # << install post
