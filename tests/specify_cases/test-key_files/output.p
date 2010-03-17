--- output.orig.spec	2010-03-17 21:15:11.000000000 +0800
+++ output.spec	2010-03-17 21:15:11.000000000 +0800
@@ -61,6 +61,8 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%doc README INST
+%{_bindir}/*
 # >> files
 # << files
 
