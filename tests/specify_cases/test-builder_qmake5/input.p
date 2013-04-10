--- ../base/testpkg.yaml	2012-07-06 23:03:05.000000000 +0000
+++ testpkg.yaml	2013-04-10 13:35:23.087449838 +0000
@@ -13,7 +13,7 @@ Description: |
     specified, plus with one sub package "devel".
 
 Configure: none
-Builder: none
+Builder: qmake5
 
 SubPackages:
     - Name: devel
