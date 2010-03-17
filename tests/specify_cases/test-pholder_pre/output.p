--- output.orig.spec	2010-03-17 21:15:16.000000000 +0800
+++ output.spec	2010-03-17 21:15:16.000000000 +0800
@@ -53,6 +53,11 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+%pre
+# >> pre
+# extra pre scripts
+# for testing
+# << pre
 
 
 
