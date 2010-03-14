--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-14 15:10:55.000000000 +0800
@@ -3,10 +3,10 @@ Summary: Sample package for spectacle te
 Version: 1.0
 Release: 1
 Group: System/Base
-License: BSD
+License:
+    - BSD
 URL: http://www.testpkg.org/
-Sources:
-    - http://www.testpkg.org/testpkg-%{version}.tar.gz
+Sources: http://www.testpkg.org/testpkg-%{version}.tar.gz
 Description: |
     Sample package for spectacle testings, which will be used as
     the base of all testings. In this YAML file, only basic keywords
