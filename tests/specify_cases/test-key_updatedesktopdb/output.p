--- output.orig.spec	2012-02-24 12:29:46.270120571 +0200
+++ output.spec	2012-02-24 12:29:46.441124425 +0200
@@ -16,6 +16,9 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): %{_bindir}/update-desktop-database
+Requires(postun): %{_bindir}/update-desktop-database
+BuildRequires:  %{_bindir}/desktop-file-install
 
 
 %description
@@ -55,12 +58,20 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+desktop-file-install --delete-original       \
+  --dir %{buildroot}%{_datadir}/applications             \
+   %{buildroot}%{_datadir}/applications/*.desktop
 
+%post
+update-desktop-database %{_datadir}/applications &> /dev/null || :
 
+%postun
+update-desktop-database %{_datadir}/applications &> /dev/null || :
 
 
 %files
 %defattr(-,root,root,-)
+%{_datadir}/applications/*.desktop
 # >> files
 # << files
 
