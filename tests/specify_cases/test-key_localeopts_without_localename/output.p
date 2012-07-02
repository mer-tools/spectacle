--- output.orig.spec	2012-07-02 15:35:08.199573778 +0300
+++ output.spec	2012-07-02 15:35:08.308573781 +0300
@@ -55,8 +55,9 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+%find_lang %{name} -gnome
 
-%files
+%files -f %{name}.lang
 %defattr(-,root,root,-)
 # >> files
 # << files
