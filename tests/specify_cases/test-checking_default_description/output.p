--- output.orig.spec	2013-04-10 18:10:26.419227490 +0000
+++ output.spec	2013-04-10 18:10:34.387287672 +0000
@@ -18,10 +18,7 @@ Source0:    http://www.testpkg.org/testp
 Source100:  testpkg.yaml
 
 %description
-Sample package for spectacle testings, which will be used as
-the base of all testings. In this YAML file, only basic keywords
-specified, plus with one sub package "devel".
-
+%{summary}.
 
 %package devel
 Summary:    Development files for %{name}
@@ -29,7 +26,7 @@ Group:      Development/Libraries
 Requires:   %{name} = %{version}-%{release}
 
 %description devel
-This package contains development files for %{name}.
+%{summary}.
 
 %prep
 %setup -q -n %{name}-%{version}
