--- output.orig.spec	2012-02-24 13:58:48.329832769 +0200
+++ output.spec	2012-02-24 13:58:48.498836573 +0200
@@ -58,6 +58,12 @@ rm -rf %{buildroot}
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
