--- output.orig.spec	2012-10-26 06:13:41.038304975 +0000
+++ output.spec	2012-10-26 06:13:41.141305195 +0000
@@ -16,6 +16,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  fdupes
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -54,6 +55,8 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+%fdupes  %{buildroot}/%{_datadir}
+
 %files
 %defattr(-,root,root,-)
 # >> files
