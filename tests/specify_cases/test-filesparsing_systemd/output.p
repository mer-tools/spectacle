--- output.orig.spec	2012-02-24 13:51:43.460267705 +0200
+++ output.spec	2012-02-24 13:51:43.634271622 +0200
@@ -16,6 +16,10 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires:   systemd
+Requires(preun): systemd
+Requires(post): systemd
+Requires(postun): systemd
 
 
 %description
@@ -29,6 +33,10 @@ specified, plus with one sub package "de
 Summary:    Development files for %{name}
 Group:      Development/Libraries
 Requires:   %{name} = %{version}-%{release}
+Requires:   systemd
+Requires(preun): systemd
+Requires(post): systemd
+Requires(postun): systemd
 
 %description devel
 This package contains development files for %{name}.
@@ -58,12 +66,34 @@ rm -rf %{buildroot}
 # << install post
 
 
+%preun
+systemctl stop abc.service
+
+%post
+systemctl daemon-reload
+systemctl reload-or-try-restart abc.service
+
+%postun
+systemctl daemon-reload
+
+%preun devel
+systemctl stop xyz.service
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
