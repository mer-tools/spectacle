--- output.orig.spec	2012-07-02 15:11:19.251535512 +0300
+++ output.spec	2012-07-02 15:12:13.125536955 +0300
@@ -16,6 +16,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  intltool
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -23,13 +24,13 @@ the base of all testings. In this YAML f
 specified, plus with one sub package "devel".
 
 
-%package devel
-Summary:    Development files for %{name}
+%package mylocale
+Summary:    My locale files for %{name}
 Group:      Development/Libraries
 Requires:   %{name} = %{version}-%{release}
 
-%description devel
-This package contains development files for %{name}.
+%description mylocale
+This package contains locale files for %{name}.
 
 
 %prep
@@ -55,13 +56,14 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+%find_lang testpkg
 
 %files
 %defattr(-,root,root,-)
 # >> files
 # << files
 
-%files devel
+%files mylocale -f testpkg.lang
 %defattr(-,root,root,-)
-# >> files devel
-# << files devel
+# >> files mylocale
+# << files mylocale
