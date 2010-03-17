--- output.orig.spec	2010-03-17 21:15:17.000000000 +0800
+++ output.spec	2010-03-17 21:15:17.000000000 +0800
@@ -52,6 +52,10 @@ rm -rf %{buildroot}
 
 # >> install post
 # << install post
+%check
+# >> check
+make check
+# << check
 
 
 
