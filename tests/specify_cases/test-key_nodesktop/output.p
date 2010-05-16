--- output.orig.spec	2010-05-16 19:00:18.000000000 +0800
+++ output.spec	2010-05-16 19:00:18.000000000 +0800
@@ -64,6 +64,7 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%{_datadir}/applications/*.desktop
 # >> files
 # << files
 
