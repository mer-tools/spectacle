--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-14 15:54:59.000000000 +0800
@@ -12,8 +12,11 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
-Configure: none
-Builder: none
+Configure: configure
+ConfigOptions:
+    - --disable-static
+    - --otheropt
+Builder: make
 
 SubPackages:
     - Name: devel
