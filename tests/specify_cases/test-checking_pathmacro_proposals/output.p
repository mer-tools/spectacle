--- output.orig.spec	2012-07-02 15:35:04.642573683 +0300
+++ output.spec	2012-07-02 15:35:04.758573686 +0300
@@ -16,6 +16,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): /sbin/install-info
+Requires(postun): /sbin/install-info
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -56,8 +58,19 @@ rm -rf %{buildroot}
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
 
