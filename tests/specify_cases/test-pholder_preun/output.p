--- output.orig.spec	2010-07-23 11:03:08.094988800 +0800
+++ output.spec	2010-07-23 11:03:08.261652945 +0800
@@ -55,6 +55,11 @@ rm -rf %{buildroot}
 # << install post
 
 
+%preun
+# >> preun
+# extra preun scripts
+# for testing
+# << preun
 
 
 
