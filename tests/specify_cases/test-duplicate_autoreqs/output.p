--- output.orig.spec	2012-07-02 15:35:06.978573745 +0300
+++ output.spec	2012-07-02 15:35:07.092573749 +0300
@@ -16,6 +16,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): /sbin/ldconfig
+Requires(postun): /sbin/ldconfig
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -56,8 +58,13 @@ rm -rf %{buildroot}
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
 
