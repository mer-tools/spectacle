--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-17 21:34:05.000000000 +0800
@@ -4,7 +4,7 @@ Version: 1.0
 Release: 1
 Group: System/Base
 License: BSD
-URL: http://www.testpkg.org/
+URL:
 Sources:
     - http://www.testpkg.org/testpkg-%{version}.tar.gz
 Description: |
@@ -14,6 +14,9 @@ Description: |
 
 Configure: none
 Builder: none
+Patches:
+Check:
+
 
 SubPackages:
     - Name: devel
