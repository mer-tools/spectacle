--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-30 17:18:27.000000000 +0800
@@ -11,6 +11,11 @@ Description: |
     Sample package for spectacle testings, which will be used as
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
+Requires:
+    - ppc:ppc-pkg
+
+PkgBR:
+    - sparc:sparc-pkg-devel
 
 Configure: none
 Builder: none
