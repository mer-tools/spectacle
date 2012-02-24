--- output.orig.spec	2012-02-24 13:47:09.139091977 +0200
+++ output.spec	2012-02-24 13:47:09.318096008 +0200
@@ -16,6 +16,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): /sbin/ldconfig
+Requires(postun): /sbin/ldconfig
 
 
 %description
@@ -58,8 +60,13 @@ rm -rf %{buildroot}
 # << install post
 
 
+%post -p /sbin/ldconfig
+
+%postun -p /sbin/ldconfig
+
 %files
 %defattr(-,root,root,-)
+%{_libdir}/*.so
 # >> files
 # << files
 
