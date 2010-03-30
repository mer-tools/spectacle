--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-30 17:16:49.000000000 +0800
@@ -12,8 +12,13 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
-Configure: none
-Builder: none
+Configure: configure
+ConfigOptions:
+    - --common-opt
+    - arm:--arm-opt
+    - ix86:--x86-opt
+
+Builder: make
 
 SubPackages:
     - Name: devel
