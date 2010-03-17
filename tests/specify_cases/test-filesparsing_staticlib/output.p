--- output.orig.spec	2010-03-17 21:15:08.000000000 +0800
+++ output.spec	2010-03-17 21:15:08.000000000 +0800
@@ -4,6 +4,7 @@
 # 
 # >> macros
 # << macros
+%define keepstatic 1
 
 Name:       testpkg
 Summary:    Sample package for spectacle testings
@@ -41,7 +42,8 @@ This package contains development files 
 # >> build pre
 # << build pre
 
-
+%configure 
+make %{?jobs:-j%jobs}
 
 # >> build post
 # << build post
@@ -49,6 +51,7 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%make_install
 
 # >> install post
 # << install post
@@ -61,6 +64,7 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%{_libdir}/*.a
 # >> files
 # << files
 
