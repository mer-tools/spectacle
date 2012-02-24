--- output.orig.spec	2012-02-24 12:36:18.176950753 +0200
+++ output.spec	2012-02-24 12:36:18.345954559 +0200
@@ -55,11 +55,12 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+%find_lang %{name} -gnome
 
 
 
 
-%files
+%files -f %{name}.lang
 %defattr(-,root,root,-)
 # >> files
 # << files
