--- output.orig.spec	2012-06-06 13:07:56.834228873 +0300
+++ output.spec	2012-06-06 13:07:57.466232002 +0300
@@ -16,6 +16,10 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires:   systemd
+Requires(preun): systemd
+Requires(post): systemd
+Requires(postun): systemd
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -27,6 +31,10 @@ specified, plus with one sub package "de
 Summary:    Development files for %{name}
 Group:      Development/Libraries
 Requires:   %{name} = %{version}-%{release}
+Requires:   systemd
+Requires(preun): systemd
+Requires(post): systemd
+Requires(postun): systemd
 
 %description devel
 This package contains development files for %{name}.
@@ -56,12 +64,38 @@ rm -rf %{buildroot}
 # << install post
 
 
+%preun
+if [ "$1" -eq 0 ]; then
+systemctl stop abc.service
+fi
+
+%post
+systemctl daemon-reload
+systemctl reload-or-try-restart abc.service
+
+%postun
+systemctl daemon-reload
+
+%preun devel
+if [ "$1" -eq 0 ]; then
+systemctl stop xyz.service
+fi
+
+%post devel
+systemctl daemon-reload
+systemctl reload-or-try-restart xyz.service
+
+%postun devel
+systemctl daemon-reload
+
 %files
 %defattr(-,root,root,-)
+/%{_lib}/systemd/system/abc.service
 # >> files
 # << files
 
 %files devel
 %defattr(-,root,root,-)
+/lib/systemd/system/xyz.service
 # >> files devel
 # << files devel
