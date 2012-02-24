--- output.orig.spec	2012-02-24 13:46:32.668270921 +0200
+++ output.spec	2012-02-24 13:46:32.840274794 +0200
@@ -58,6 +58,11 @@ rm -rf %{buildroot}
 # << install post
 
 
+%check
+# >> check
+make check
+# << check
+
 %files
 %defattr(-,root,root,-)
 # >> files
