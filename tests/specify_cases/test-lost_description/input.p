--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-14 17:33:38.000000000 +0800
@@ -7,11 +7,6 @@ License: BSD
 URL: http://www.testpkg.org/
 Sources:
     - http://www.testpkg.org/testpkg-%{version}.tar.gz
-Description: |
-    Sample package for spectacle testings, which will be used as
-    the base of all testings. In this YAML file, only basic keywords
-    specified, plus with one sub package "devel".
-
 Configure: none
 Builder: none
 
@@ -19,4 +14,3 @@ SubPackages:
     - Name: devel
       Summary: Development files for %{name}
       Group: Development/Libraries
-      Description: This package contains development files for %{name}.
