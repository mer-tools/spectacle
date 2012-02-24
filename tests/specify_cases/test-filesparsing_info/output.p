--- output.orig.spec	2012-02-24 13:48:35.999047431 +0200
+++ output.spec	2012-02-24 13:48:36.171051303 +0200
@@ -16,6 +16,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): /sbin/install-info
+Requires(postun): /sbin/install-info
 
 
 %description
@@ -58,8 +60,17 @@ rm -rf %{buildroot}
 # << install post
 
 
+%post
+%install_info --info-dir=%_infodir %{_infodir}/*.info.gz
+
+%postun
+if [ $1 = 0 ] ;then
+%install_info_delete --info-dir=%{_infodir} %{_infodir}/*.info.gz
+fi
+
 %files
 %defattr(-,root,root,-)
+%{_infodir}/*.info.gz
 # >> files
 # << files
 
