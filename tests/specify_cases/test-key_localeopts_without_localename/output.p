--- output.orig.spec	2012-02-24 13:54:39.837238459 +0200
+++ output.spec	2012-02-24 13:54:40.010242353 +0200
@@ -57,8 +57,9 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+%find_lang %{name} -gnome
 
-%files
+%files -f %{name}.lang
 %defattr(-,root,root,-)
 # >> files
 # << files
