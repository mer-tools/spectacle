--- output.orig.spec	2010-07-23 11:02:42.067225740 +0800
+++ output.spec	2010-07-23 11:02:42.215377186 +0800
@@ -57,6 +57,11 @@ rm -rf %{buildroot}
 
 
 
+%postun
+# >> postun
+# customized postun scripts here
+# for testing
+# << postun
 
 
 
