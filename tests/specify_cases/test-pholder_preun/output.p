--- output.orig.spec	2012-07-02 15:35:08.912573797 +0300
+++ output.spec	2012-07-02 15:35:09.027573800 +0300
@@ -56,6 +56,12 @@ rm -rf %{buildroot}
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
