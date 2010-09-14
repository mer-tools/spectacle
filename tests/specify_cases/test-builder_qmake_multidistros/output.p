--- output.orig.spec	2010-09-14 16:16:17.659225984 +0800
+++ output.spec	2010-09-14 16:16:34.681161185 +0800
@@ -14,6 +14,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRoot:  %{_tmppath}/%{name}-%{version}-build
 
 
 %description
@@ -42,14 +43,24 @@ This package contains development files
 # >> build pre
 # << build pre
 
-
+%if 0%{?moblin_version}
+%qmake
+%else
+qmake-qt4 install_prefix=/usr
+%endif
+make %{?jobs:-j%jobs}
 
 # >> build post
 # << build post
 %install
-rm -rf %{buildroot}
+rm -rf $RPM_BUILD_ROOT
 # >> install pre
 # << install pre
+%if 0%{?moblin_version}
+%qmake_install
+%else
+%makeinstall
+%endif
 
 # >> install post
 # << install post
