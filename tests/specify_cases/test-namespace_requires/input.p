--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-30 17:11:48.000000000 +0800
@@ -11,6 +11,10 @@ Description: |
     Sample package for spectacle testings, which will be used as
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
+Requires:
+    - arm:arm-pkgs
+    - ix86:x86-pkgs
+    - common-pkgs
 
 Configure: none
 Builder: none
@@ -20,3 +24,7 @@ SubPackages:
       Summary: Development files for %{name}
       Group: Development/Libraries
       Description: This package contains development files for %{name}.
+      Requires:
+        - arm:arm-pkgs
+        - ix86:x86-pkgs
+        - common-pkgs
