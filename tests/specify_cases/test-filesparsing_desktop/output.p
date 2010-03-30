--- output.orig.spec	2010-03-30 19:56:35.000000000 +0800
+++ output.spec	2010-03-30 19:56:35.000000000 +0800
@@ -14,6 +14,9 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): desktop-file-utils
+Requires(postun): desktop-file-utils
+BuildRequires:  desktop-file-utils
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -52,10 +55,17 @@ rm -rf %{buildroot}
 
 # >> install post
 # << install post
+desktop-file-install --delete-original       \
+  --dir %{buildroot}%{_datadir}/applications             \
+   %{buildroot}%{_datadir}/applications/*
 
 
 
+%post
+update-desktop-database %{_datadir}/applications &> /dev/null || :
 
+%postun
+update-desktop-database %{_datadir}/applications &> /dev/null || :
 
 
 
@@ -63,6 +73,7 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%{_datadir}/*.desktop
 # >> files
 # << files
 
