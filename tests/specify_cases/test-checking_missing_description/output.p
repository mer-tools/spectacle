--- output.orig.spec	2010-03-17 21:15:14.000000000 +0800
+++ output.spec	2010-03-17 21:15:14.000000000 +0800
@@ -16,10 +16,7 @@ Source0:    http://www.testpkg.org/testp
 Source100:  testpkg.yaml
 
 %description
-Sample package for spectacle testings, which will be used as
-the base of all testings. In this YAML file, only basic keywords
-specified, plus with one sub package "devel".
-
+Description: %{summary}
 
 
 %package devel
@@ -28,7 +25,7 @@ Group:      Development/Libraries
 Requires:   %{name} = %{version}-%{release}
 
 %description devel
-This package contains development files for %{name}.
+Description: %{summary}
 
 
 %prep
