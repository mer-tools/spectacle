--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-05-18 20:03:30.000000000 +0800
@@ -12,8 +12,11 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
-Configure: none
-Builder: none
+Builder: python
+BuildArch: noarch
+
+Files:
+    - "%{python_sitearch}/*"
 
 SubPackages:
     - Name: devel
