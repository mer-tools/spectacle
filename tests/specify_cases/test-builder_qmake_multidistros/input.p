--- ../base/testpkg.yaml	2010-09-07 11:40:02.000000000 +0800
+++ testpkg.yaml	2010-09-14 16:16:34.549150340 +0800
@@ -12,8 +12,8 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
-Configure: none
-Builder: none
+Builder: qmake
+SupportOtherDistros: yes
 
 SubPackages:
     - Name: devel
