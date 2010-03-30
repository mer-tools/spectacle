--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-30 17:14:41.000000000 +0800
@@ -12,6 +12,11 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
+PkgBR:
+    - common-br
+    - arm:arm-br
+    - ix86:x86-br
+
 Configure: none
 Builder: none
 
