--- output.orig.spec	2012-10-26 06:14:24.219368272 +0000
+++ output.spec	2012-10-26 06:14:24.323368496 +0000
@@ -16,6 +16,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  intltool
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -54,7 +55,9 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
-%files
+%find_lang testpkg
+
+%files -f testpkg.lang
 %defattr(-,root,root,-)
 # >> files
 # << files
