--- output.orig.spec	2010-05-16 19:05:10.000000000 +0800
+++ output.spec	2010-05-16 19:05:10.000000000 +0800
@@ -57,6 +57,11 @@ rm -rf %{buildroot}
 
 
 
+%postun
+# >> postun
+# customized postun scripts here
+# for testing
+# << postun
 
 
 
