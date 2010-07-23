--- output.orig.spec	2010-07-23 11:18:42.942304765 +0800
+++ output.spec	2010-07-23 11:18:54.444732273 +0800
@@ -5,6 +5,7 @@
 # >> macros
 # << macros
 
+%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
 Name:       testpkg
 Summary:    Sample package for spectacle testings
 Version:    1.0
@@ -42,7 +43,7 @@ This package contains development files 
 # >> build pre
 # << build pre
 
-
+CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
 
 # >> build post
 # << build post
@@ -50,6 +51,7 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%{__python} setup.py install --root=%{buildroot} -O1
 
 # >> install post
 # << install post
