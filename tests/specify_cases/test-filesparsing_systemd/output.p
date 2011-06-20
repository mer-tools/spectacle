--- output.orig.spec	2011-06-20 17:13:08.859595672 +0800
+++ output.spec	2011-06-20 17:13:08.980595440 +0800
@@ -14,6 +14,10 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires:   systemd
+Requires(preun): systemd
+Requires(post): systemd
+Requires(postun): systemd
 
 
 %description
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
@@ -55,21 +63,37 @@ rm -rf %{buildroot}
 # << install post
 
 
+%preun
+systemctl stop abc.service
 
+%post
+systemctl daemon-reload
+systemctl reload-or-try-restart abc.service
 
+%postun
+systemctl daemon-reload
 
 
+%preun devel
+systemctl stop xyz.service
 
+%post devel
+systemctl daemon-reload
+systemctl reload-or-try-restart xyz.service
 
+%postun devel
+systemctl daemon-reload
 
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
 
