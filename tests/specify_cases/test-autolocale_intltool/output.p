--- output.orig.spec	2010-03-18 16:06:56.000000000 +0800
+++ output.spec	2010-03-18 16:07:07.000000000 +0800
@@ -14,6 +14,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  intltool
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -52,6 +53,7 @@ rm -rf %{buildroot}
 
 # >> install post
 # << install post
+%find_lang testpkg
 
 
 
@@ -59,7 +61,7 @@ rm -rf %{buildroot}
 
 
 
-%files
+%files -f testpkg.lang
 %defattr(-,root,root,-)
 # >> files
 # << files
