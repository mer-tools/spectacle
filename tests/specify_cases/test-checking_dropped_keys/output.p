--- output.orig.spec	2010-03-17 21:15:04.000000000 +0800
+++ output.spec	2010-03-17 21:15:05.000000000 +0800
@@ -61,6 +61,8 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%doc README
+%doc DOC
 # >> files
 # << files
 
