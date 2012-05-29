--- output.orig.spec	2012-05-29 18:29:53.547913017 +0300
+++ output.spec	2012-05-29 18:29:54.183916168 +0300
@@ -16,6 +16,9 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): %{_bindir}/update-desktop-database
+Requires(postun): %{_bindir}/update-desktop-database
+BuildRequires:  desktop-file-utils
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -55,9 +58,19 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+desktop-file-install --delete-original       \
+  --dir %{buildroot}%{_datadir}/applications             \
+   %{buildroot}%{_datadir}/applications/*.desktop
+
+%post
+update-desktop-database %{_datadir}/applications &> /dev/null || :
+
+%postun
+update-desktop-database %{_datadir}/applications &> /dev/null || :
 
 %files
 %defattr(-,root,root,-)
+%{_datadir}/applications/*.desktop
 # >> files
 # << files
 
