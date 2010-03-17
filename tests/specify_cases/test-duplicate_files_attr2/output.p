--- output.orig.spec	2010-03-17 21:15:06.000000000 +0800
+++ output.spec	2010-03-17 21:15:06.000000000 +0800
@@ -62,6 +62,7 @@ rm -rf %{buildroot}
 %files
 %defattr(-,root,root,-)
 # >> files
+%{_bindir}/*
 # << files
 
 
