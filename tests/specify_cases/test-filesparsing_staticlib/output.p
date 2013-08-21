--- output.orig.spec	2010-06-21 16:41:15.000000000 +0800
+++ output.spec	2010-06-21 16:41:15.000000000 +0800
@@ -4,6 +4,7 @@
 # 
 # >> macros
 # << macros
+%define keepstatic 1
 
 Name:       testpkg
 Summary:    Sample package for spectacle testings
@@ -42,7 +43,8 @@ This package contains development files 
 # >> build pre
 # << build pre
 
-
+%configure 
+make %{?_smp_mflags}
 
 # >> build post
 # << build post
@@ -50,6 +52,7 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%make_install
 
 # >> install post
 # << install post
@@ -64,6 +67,7 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%{_libdir}/*.a
 # >> files
 # << files
 
