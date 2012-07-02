--- output.orig.spec	2012-07-02 15:35:08.430573784 +0300
+++ output.spec	2012-07-02 15:35:08.546573787 +0300
@@ -56,6 +56,12 @@ rm -rf %{buildroot}
 # << install post
 
 
+%postun
+# >> postun
+# customized postun scripts here
+# for testing
+# << postun
+
 %files
 %defattr(-,root,root,-)
 # >> files
