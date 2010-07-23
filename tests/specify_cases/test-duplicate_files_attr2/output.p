--- output.orig.spec	2010-07-23 11:06:24.794056323 +0800
+++ output.spec	2010-07-23 11:06:24.961431494 +0800
@@ -65,6 +65,7 @@ rm -rf %{buildroot}
 %files
 %defattr(-,root,root,-)
 # >> files
+%{_bindir}/*
 # << files
 
 
