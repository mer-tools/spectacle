--- output.orig.spec	2010-03-17 21:15:14.000000000 +0800
+++ output.spec	2010-03-17 21:15:14.000000000 +0800
@@ -52,6 +52,7 @@ rm -rf %{buildroot}
 
 # >> install post
 # << install post
+%find_lang %{name} -gnome
 
 
 
@@ -59,7 +60,7 @@ rm -rf %{buildroot}
 
 
 
-%files
+%files -f %{name}.lang
 %defattr(-,root,root,-)
 # >> files
 # << files
