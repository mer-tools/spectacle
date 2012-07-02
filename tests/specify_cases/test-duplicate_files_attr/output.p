--- output.orig.spec	2012-07-02 15:35:07.497573761 +0300
+++ output.spec	2012-07-02 15:35:07.609573762 +0300
@@ -58,6 +58,7 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%{_bindir}/*
 # >> files
 # << files
 
