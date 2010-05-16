--- output.orig.spec	2010-05-16 19:01:30.000000000 +0800
+++ output.spec	2010-05-16 19:01:30.000000000 +0800
@@ -14,6 +14,9 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): desktop-file-utils
+Requires(postun): desktop-file-utils
+BuildRequires:  desktop-file-utils
 
 
 %description
@@ -53,10 +56,17 @@ rm -rf %{buildroot}
 
 # >> install post
 # << install post
+desktop-file-install --delete-original       \
+  --dir %{buildroot}%{_datadir}/applications             \
+   %{buildroot}%{_datadir}/applications/*.desktop
 
 
 
+%post
+update-desktop-database %{_datadir}/applications &> /dev/null || :
 
+%postun
+update-desktop-database %{_datadir}/applications &> /dev/null || :
 
 
 
@@ -64,6 +74,7 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%{_datadir}/applications/*.desktop
 # >> files
 # << files
 
