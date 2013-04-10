--- ../base/testpkg.yaml	2010-09-07 11:40:02.000000000 +0800
+++ testpkg.yaml	2010-09-17 11:00:19.520567286 +0800
@@ -12,8 +12,11 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
-Configure: none
-Builder: none
+Builder: qmake
+QMakeOptions:
+    - arm:--arm-only
+    - ix86:--ix86-only
+    - --common-one
 
 SubPackages:
     - Name: devel
