--- output.orig.spec	2012-07-02 15:35:02.519573626 +0300
+++ output.spec	2012-07-02 15:35:02.629573629 +0300
@@ -58,6 +58,8 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%doc README
+%doc DOC
 # >> files
 # << files
 
