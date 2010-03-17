--- output.orig.spec	2010-03-17 21:15:10.000000000 +0800
+++ output.spec	2010-03-17 21:15:10.000000000 +0800
@@ -9,6 +9,7 @@ Name:       testpkg
 Summary:    Sample package for spectacle testings
 Version:    1.0
 Release:    1
+Epoch:      1
 Group:      System/Base
 License:    BSD
 URL:        http://www.testpkg.org/
@@ -25,7 +26,7 @@ specified, plus with one sub package "de
 %package devel
 Summary:    Development files for %{name}
 Group:      Development/Libraries
-Requires:   %{name} = %{version}-%{release}
+Requires:   %{name} = %{epoch}:%{version}-%{release}
 
 %description devel
 This package contains development files for %{name}.
