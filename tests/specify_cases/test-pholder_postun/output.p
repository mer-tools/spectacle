--- output.orig.spec	2010-03-17 21:15:16.000000000 +0800
+++ output.spec	2010-03-17 21:15:16.000000000 +0800
@@ -56,6 +56,11 @@ rm -rf %{buildroot}
 
 
 
+%postun
+# >> postun
+# customized postun scripts here
+# for testing
+# << postun
 
 
 
