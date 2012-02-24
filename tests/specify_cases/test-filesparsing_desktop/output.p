--- output.orig.spec	2012-02-24 13:47:54.207106581 +0200
+++ output.spec	2012-02-24 13:47:54.388110654 +0200
@@ -16,6 +16,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  %{_bindir}/desktop-file-install
 
 
 %description
@@ -57,9 +58,13 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+desktop-file-install --delete-original       \
+  --dir %{buildroot}%{_datadir}/applications             \
+   %{buildroot}%{_datadir}/applications/*.desktop
 
 %files
 %defattr(-,root,root,-)
+%{_datadir}/applications/*.desktop
 # >> files
 # << files
 
