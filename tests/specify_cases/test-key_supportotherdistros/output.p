--- output.orig.spec	2012-02-24 13:57:10.149622436 +0200
+++ output.spec	2012-02-24 13:57:10.318626241 +0200
@@ -8,6 +8,7 @@ Name:       testpkg
 # >> macros
 # << macros
 
+%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
 Summary:    Sample package for spectacle testings
 Version:    1.0
 Release:    1
@@ -16,6 +17,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRoot:  %{_tmppath}/%{name}-%{version}-build
 
 
 %description
@@ -44,15 +46,20 @@ This package contains development files 
 # >> build pre
 # << build pre
 
-
+CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
 
 # >> build post
 # << build post
 
 %install
-rm -rf %{buildroot}
+rm -rf $RPM_BUILD_ROOT
 # >> install pre
 # << install pre
+%if 0%{?suse_version}
+%{__python} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix}
+%else
+%{__python} setup.py install --root=$RPM_BUILD_ROOT -O1
+%endif
 
 # >> install post
 # << install post
