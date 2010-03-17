--- output.orig.spec	2010-03-17 21:15:15.000000000 +0800
+++ output.spec	2010-03-17 21:15:15.000000000 +0800
@@ -14,6 +14,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+AutoReq: 0
+AutoProv: 0
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -25,6 +27,7 @@ specified, plus with one sub package "de
 %package devel
 Summary:    Development files for %{name}
 Group:      Development/Libraries
+AutoReq:    0
 Requires:   %{name} = %{version}-%{release}
 
 %description devel
