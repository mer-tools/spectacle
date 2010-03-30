--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-30 17:13:43.000000000 +0800
@@ -7,6 +7,10 @@ License: BSD
 URL: http://www.testpkg.org/
 Sources:
     - http://www.testpkg.org/testpkg-%{version}.tar.gz
+Patches:
+    - common-patch
+    - arm:arm-only-patch
+    - ix86:x86-only-patch
 Description: |
     Sample package for spectacle testings, which will be used as
     the base of all testings. In this YAML file, only basic keywords
