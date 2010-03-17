--- output.orig.spec	2010-03-17 21:15:07.000000000 +0800
+++ output.spec	2010-03-17 21:15:07.000000000 +0800
@@ -14,6 +14,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post):  /sbin/ldconfig
+Requires(postun):  /sbin/ldconfig
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -55,12 +57,15 @@ rm -rf %{buildroot}
 
 
 
+%post -p /sbin/ldconfig
 
+%postun -p /sbin/ldconfig
 
 
 
 %files
 %defattr(-,root,root,-)
+%{_libdir}/*.so
 # >> files
 # << files
 
