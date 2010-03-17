--- output.orig.spec	2010-03-17 21:15:10.000000000 +0800
+++ output.spec	2010-03-17 21:15:11.000000000 +0800
@@ -49,6 +49,9 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+# extra install scripts in %install
+# etc.
+
 
 # >> install post
 # << install post
