--- output.orig.spec	2012-07-02 14:39:53.682485018 +0300
+++ output.spec	2012-07-02 14:40:13.041485537 +0300
@@ -55,8 +55,9 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+%find_lang localenametest
 
-%files
+%files -f localenametest.lang
 %defattr(-,root,root,-)
 # >> files
 # << files
