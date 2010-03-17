--- output.orig.spec	2010-03-17 21:31:52.000000000 +0800
+++ output.spec	2010-03-17 21:31:52.000000000 +0800
@@ -54,6 +54,11 @@ rm -rf %{buildroot}
 # << install post
 
 
+%preun
+# >> preun
+# extra preun scripts
+# for testing
+# << preun
 
 
 
