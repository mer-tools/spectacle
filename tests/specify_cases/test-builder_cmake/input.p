--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-07-23 11:16:29.493919869 +0800
@@ -12,8 +12,7 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
-Configure: none
-Builder: none
+Builder: cmake
 
 SubPackages:
     - Name: devel
