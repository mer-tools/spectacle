--- output.orig.spec	2013-04-10 18:18:01.830667239 +0000
+++ output.spec	2013-04-10 18:18:57.924090928 +0000
@@ -16,6 +16,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(post): /sbin/ldconfig
+Requires(postun): /sbin/ldconfig
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -23,6 +25,16 @@ the base of all testings. In this YAML f
 specified, plus with one sub package "devel".
 
 
+%package subpkg
+Summary:    Development files for %{name}
+Group:      Development/Libraries
+Requires:   %{name} = %{version}-%{release}
+Requires(post): /sbin/ldconfig
+Requires(postun): /sbin/ldconfig
+
+%description subpkg
+This package contains development files for %{name}.
+
 %package devel
 Summary:    Development files for %{name}
 Group:      Development/Libraries
@@ -54,12 +66,28 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+%post -p /sbin/ldconfig
+
+%postun -p /sbin/ldconfig
+
+%post subpkg -p /sbin/ldconfig
+
+%postun subpkg -p /sbin/ldconfig
+
 %files
 %defattr(-,root,root,-)
+%{_libdir}/*.so
 # >> files
 # << files
 
+%files subpkg
+%defattr(-,root,root,-)
+%{_libdir}/sub*.so
+# >> files subpkg
+# << files subpkg
+
 %files devel
 %defattr(-,root,root,-)
+%{_libdir}/devel*.so
 # >> files devel
 # << files devel
