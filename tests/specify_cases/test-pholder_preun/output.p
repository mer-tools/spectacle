--- output.orig.spec	2012-02-24 12:27:24.678928747 +0200
+++ output.spec	2012-02-24 12:27:24.850932626 +0200
@@ -55,6 +55,11 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+%preun
+# >> preun
+# extra preun scripts
+# for testing
+# << preun
 
 
 
