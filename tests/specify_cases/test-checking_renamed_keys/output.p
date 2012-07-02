--- output.orig.spec	2012-07-02 15:35:05.353573702 +0300
+++ output.spec	2012-07-02 15:35:05.465573705 +0300
@@ -56,6 +56,11 @@ rm -rf %{buildroot}
 # << install post
 
 
+%check
+# >> check
+make check
+# << check
+
 %files
 %defattr(-,root,root,-)
 # >> files
