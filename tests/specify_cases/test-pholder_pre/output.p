--- output.orig.spec	2012-02-24 13:59:11.968364944 +0200
+++ output.spec	2012-02-24 13:59:12.140368816 +0200
@@ -58,6 +58,12 @@ rm -rf %{buildroot}
 # << install post
 
 
+%pre
+# >> pre
+# extra pre scripts
+# for testing
+# << pre
+
 %files
 %defattr(-,root,root,-)
 # >> files
