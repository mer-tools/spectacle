--- output.orig.spec	2012-02-24 13:54:04.146434954 +0200
+++ output.spec	2012-02-24 13:54:04.317438804 +0200
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
