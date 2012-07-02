--- output.orig.spec	2012-07-02 15:35:02.996573639 +0300
+++ output.spec	2012-07-02 15:35:03.108573642 +0300
@@ -8,6 +8,7 @@ Name:       testpkg
 # >> macros
 # << macros
 
+%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
 Summary:    Sample package for spectacle testings
 Version:    1.0
 Release:    1
@@ -42,7 +43,7 @@ This package contains development files
 # >> build pre
 # << build pre
 
-
+CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
 
 # >> build post
 # << build post
@@ -51,6 +52,7 @@ This package contains development files
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%{__python} setup.py install --root=%{buildroot} -O1
 
 # >> install post
 # << install post
