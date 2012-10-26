--- output.orig.spec	2012-10-26 06:14:15.071355077 +0000
+++ output.spec	2012-10-26 06:14:15.173355296 +0000
@@ -16,6 +16,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  desktop-file-utils
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -54,8 +55,13 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+desktop-file-install --delete-original       \
+  --dir %{buildroot}%{_datadir}/applications             \
+   %{buildroot}%{_datadir}/applications/*.desktop
+
 %files
 %defattr(-,root,root,-)
+%{_datadir}/applications/*.desktop
 # >> files
 # << files
 
