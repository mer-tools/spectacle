--- output.orig.spec	2012-02-24 13:45:31.914903204 +0200
+++ output.spec	2012-02-24 13:45:32.101907413 +0200
@@ -16,6 +16,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): /sbin/install-info
+Requires(postun): /sbin/install-info
 
 
 %description
@@ -58,8 +60,19 @@ rm -rf %{buildroot}
 # << install post
 
 
+%post
+%install_info --info-dir=%_infodir /usr/share/info/info.gz
+
+%postun
+if [ $1 = 0 ] ;then
+%install_info_delete --info-dir=%{_infodir} /usr/share/info/info.gz
+fi
+
 %files
 %defattr(-,root,root,-)
+/usr/bin/abc
+/usr/share/info/info.gz
+/usr/share/testpkg/api
 # >> files
 # << files
 
