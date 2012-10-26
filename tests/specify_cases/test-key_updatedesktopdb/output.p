--- output.orig.spec	2012-10-26 06:12:58.920246810 +0000
+++ output.spec	2012-10-26 06:12:59.021247026 +0000
@@ -16,6 +16,9 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): %{_bindir}/update-desktop-database
+Requires(postun): %{_bindir}/update-desktop-database
+BuildRequires:  desktop-file-utils
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -54,8 +57,19 @@ rm -rf %{buildroot}
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
+
 %files
 %defattr(-,root,root,-)
+%{_datadir}/applications/*.desktop
 # >> files
 # << files
 
