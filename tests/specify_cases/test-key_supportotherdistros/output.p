--- output.orig.spec	2010-05-16 19:03:04.000000000 +0800
+++ output.spec	2010-05-16 19:03:04.000000000 +0800
@@ -5,6 +5,7 @@
 # >> macros
 # << macros
 
+%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
 Name:       testpkg
 Summary:    Sample package for spectacle testings
 Version:    1.0
@@ -14,6 +15,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRoot:  %{_tmppath}/%{name}-%{version}-build
 
 
 %description
@@ -42,14 +44,19 @@ This package contains development files 
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
