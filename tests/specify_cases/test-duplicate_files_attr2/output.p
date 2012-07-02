--- output.orig.spec	2012-07-02 15:35:07.730573766 +0300
+++ output.spec	2012-07-02 15:35:07.843573769 +0300
@@ -59,6 +59,7 @@ rm -rf %{buildroot}
 %files
 %defattr(-,root,root,-)
 # >> files
+%{_bindir}/*
 # << files
 
 %files devel
