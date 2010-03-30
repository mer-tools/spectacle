--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-14 15:02:15.000000000 +0800
@@ -12,6 +12,8 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
+PkgBR:
+    - libX11-devel
 Configure: none
 Builder: none
 
