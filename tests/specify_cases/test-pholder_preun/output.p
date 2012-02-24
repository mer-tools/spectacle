--- output.orig.spec	2012-02-24 13:59:32.835834735 +0200
+++ output.spec	2012-02-24 13:59:33.006838584 +0200
@@ -58,6 +58,12 @@ rm -rf %{buildroot}
 # << install post
 
 
+%preun
+# >> preun
+# extra preun scripts
+# for testing
+# << preun
+
 %files
 %defattr(-,root,root,-)
 # >> files
