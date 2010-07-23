--- output.orig.spec	2010-07-23 11:02:56.853990880 +0800
+++ output.spec	2010-07-23 11:02:57.007028539 +0800
@@ -54,6 +54,11 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+%pre
+# >> pre
+# extra pre scripts
+# for testing
+# << pre
 
 
 
