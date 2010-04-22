--- output.orig.spec	2010-04-22 19:12:21.000000000 +0800
+++ output.spec	2010-04-22 19:12:37.000000000 +0800
@@ -63,6 +63,7 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%{_datadir}/*.desktop
 # >> files
 # << files
 
