--- output.orig.spec	2010-03-17 21:15:03.000000000 +0800
+++ output.spec	2010-03-17 21:15:03.000000000 +0800
@@ -5,6 +5,7 @@
 # >> macros
 # << macros
 
+%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
 Name:       testpkg
 Summary:    Sample package for spectacle testings
 Version:    1.0
@@ -41,7 +42,7 @@ This package contains development files 
 # >> build pre
 # << build pre
 
-
+CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
 
 # >> build post
 # << build post
@@ -49,6 +50,7 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%{__python} setup.py install --root=%{buildroot} -O1
 
 # >> install post
 # << install post
