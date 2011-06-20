--- output.orig.spec	2011-06-20 17:05:38.468485134 +0800
+++ output.spec	2011-06-20 17:06:35.907678856 +0800
@@ -14,6 +14,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): /sbin/install-info
+Requires(postun): /sbin/install-info
 
 
 %description
@@ -56,7 +58,13 @@ rm -rf %{buildroot}
 
 
 
+%post
+%install_info --info-dir=%_infodir /usr/share/info/info.gz
 
+%postun
+if [ $1 = 0 ] ;then
+%install_info_delete --info-dir=%{_infodir} /usr/share/info/info.gz
+fi
 
 
 
@@ -64,6 +72,9 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+/usr/bin/abc
+/usr/share/info/info.gz
+/usr/share/testpkg/api
 # >> files
 # << files
 
