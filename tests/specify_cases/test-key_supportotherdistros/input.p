--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-14 17:54:17.000000000 +0800
@@ -13,7 +13,8 @@ Description: |
     specified, plus with one sub package "devel".
 
 Configure: none
-Builder: none
+Builder: python
+SupportOtherDistros: yes
 
 SubPackages:
     - Name: devel
