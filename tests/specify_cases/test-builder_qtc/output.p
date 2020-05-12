--- output.orig.spec
+++ output.spec
@@ -8,6 +8,10 @@
 # >> macros
 # << macros
 
+%{!?qtc_qmake:%define qtc_qmake %qmake}
+%{!?qtc_qmake5:%define qtc_qmake5 %qmake5}
+%{!?qtc_make:%define qtc_make make}
+%{?qtc_builddir:%define _builddir %qtc_builddir}
 Summary:    Sample package for spectacle testings
 Version:    1.0
 Release:    1
@@ -41,7 +45,9 @@
 # >> build pre
 # << build pre
 
+%qtc_qmake 
 
+%qtc_make %{?_smp_mflags}
 
 # >> build post
 # << build post
@@ -50,6 +56,7 @@
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%qmake_install
 
 # >> install post
 # << install post
