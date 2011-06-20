--- output.orig.spec	2011-06-20 16:48:59.504678925 +0800
+++ output.spec	2011-06-20 16:50:04.992678935 +0800
@@ -64,6 +64,13 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%ifarch %{arm}
+%{_bin}/testpkg-arm
+%endif
+%ifarch %{ix86}
+%{_bin}/testpkg-ix86
+%endif
+%{_bin}/testpkg
 # >> files
 # << files
 
