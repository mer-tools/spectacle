--- output.orig.spec	2010-03-17 21:15:09.000000000 +0800
+++ output.spec	2010-03-17 21:15:09.000000000 +0800
@@ -25,7 +25,6 @@ specified, plus with one sub package "de
 %package devel
 Summary:    Development files for %{name}
 Group:      Development/Libraries
-Requires:   %{name} = %{version}-%{release}
 
 %description devel
 This package contains development files for %{name}.
