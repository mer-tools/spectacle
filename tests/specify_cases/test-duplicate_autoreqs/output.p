--- output.orig.spec	2010-03-30 19:58:04.000000000 +0800
+++ output.spec	2010-03-30 19:58:43.000000000 +0800
@@ -14,6 +14,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): /sbin/ldconfig
+Requires(postun): /sbin/ldconfig
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -55,7 +57,9 @@ rm -rf %{buildroot}
 
 
 
+%post -p /sbin/ldconfig
 
+%postun -p /sbin/ldconfig
 
 
 
@@ -63,6 +67,7 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%{_libdir}/*.so
 # >> files
 # << files
 
