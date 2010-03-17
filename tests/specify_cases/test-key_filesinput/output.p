--- output.orig.spec	2010-03-17 21:15:11.000000000 +0800
+++ output.spec	2010-03-17 21:15:11.000000000 +0800
@@ -59,7 +59,7 @@ rm -rf %{buildroot}
 
 
 
-%files
+%files -f morefiles.lst
 %defattr(-,root,root,-)
 # >> files
 # << files
