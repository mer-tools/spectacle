--- output.orig.spec	2012-07-02 15:35:08.668573791 +0300
+++ output.spec	2012-07-02 15:35:08.785573794 +0300
@@ -56,6 +56,12 @@ rm -rf %{buildroot}
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
