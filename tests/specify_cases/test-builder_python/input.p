--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-11 23:39:01.000000000 +0800
@@ -13,7 +13,7 @@ Description: |
     specified, plus with one sub package "devel".
 
 Configure: none
-Builder: none
+Builder: python3
 
 SubPackages:
     - Name: devel
