--- ../base/testpkg.yaml	2012-07-06 23:03:05.000000000 +0000
+++ testpkg.yaml	2013-04-10 18:10:34.280286864 +0000
@@ -7,10 +7,6 @@ License: BSD
 URL: http://www.testpkg.org/
 Sources:
     - http://www.testpkg.org/testpkg-%{version}.tar.gz
-Description: |
-    Sample package for spectacle testings, which will be used as
-    the base of all testings. In this YAML file, only basic keywords
-    specified, plus with one sub package "devel".
 
 Configure: none
 Builder: none
@@ -19,4 +15,3 @@ SubPackages:
     - Name: devel
       Summary: Development files for %{name}
       Group: Development/Libraries
-      Description: This package contains development files for %{name}.
