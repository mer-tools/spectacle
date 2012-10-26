--- output.orig.spec	2012-10-26 06:13:48.321315853 +0000
+++ output.spec	2012-10-26 06:13:48.423316071 +0000
@@ -54,7 +54,9 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
-%files
+%find_lang %{name} -gnome
+
+%files -f %{name}.lang
 %defattr(-,root,root,-)
 # >> files
 # << files
