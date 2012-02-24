--- output.orig.spec	2012-02-24 13:20:32.976097986 +0200
+++ output.spec	2012-02-24 13:20:33.149101909 +0200
@@ -16,6 +16,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  intltool
 
 
 %description
@@ -55,11 +56,12 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+%find_lang testpkg
 
 
 
 
-%files
+%files -f testpkg.lang
 %defattr(-,root,root,-)
 # >> files
 # << files
