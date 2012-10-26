--- output.orig.spec	2012-10-26 06:13:57.018328422 +0000
+++ output.spec	2012-10-26 06:13:57.118328636 +0000
@@ -54,7 +54,9 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
-%files
+%find_lang localenametest
+
+%files -f localenametest.lang
 %defattr(-,root,root,-)
 # >> files
 # << files
