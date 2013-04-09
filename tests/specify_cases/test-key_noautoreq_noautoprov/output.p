--- output.orig.spec	2013-04-09 05:34:11.839030534 +0000
+++ output.spec	2013-04-09 05:34:11.941031222 +0000
@@ -16,6 +16,9 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+AutoReq:    0
+AutoReqProv:    0
+AutoProv:   0
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -26,6 +29,9 @@ specified, plus with one sub package "de
 %package devel
 Summary:    Development files for %{name}
 Group:      Development/Libraries
+AutoReq:    0
+AutoProv:   0
+AutoReqProv:    0
 Requires:   %{name} = %{version}-%{release}
 
 %description devel
