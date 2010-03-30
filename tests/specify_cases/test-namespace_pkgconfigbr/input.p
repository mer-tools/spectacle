--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-30 17:15:43.000000000 +0800
@@ -12,6 +12,11 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
+PkgConfigBR:
+    - common-pkgcfg
+    - arm:arm-pkgcfg >= 0.11
+    - ix86:x86-pkgcfg >= %{xxx_version}
+
 Configure: none
 Builder: none
 
