--- ../base/testpkg.yaml	2010-09-07 11:40:02.000000000 +0800
+++ testpkg.yaml	2010-09-17 10:57:35.131317604 +0800
@@ -12,8 +12,11 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
-Configure: none
-Builder: none
+Configure: configure
+ConfigOptions:
+    - --yes-one
+    - --no-two
+Builder: make
 
 SubPackages:
     - Name: devel
