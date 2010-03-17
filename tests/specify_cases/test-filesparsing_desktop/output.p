--- output.orig.spec	2010-03-17 21:15:07.000000000 +0800
+++ output.spec	2010-03-17 21:15:07.000000000 +0800
@@ -14,6 +14,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires: desktop-file-utils
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -52,6 +53,9 @@ rm -rf %{buildroot}
 
 # >> install post
 # << install post
+desktop-file-install --delete-original       \
+  --dir %{buildroot}%{_datadir}/applications             \
+   %{buildroot}%{_datadir}/applications/*
 
 
 
@@ -61,6 +65,7 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%{_datadir}/*.desktop
 # >> files
 # << files
 
