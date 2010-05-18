--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-05-18 20:04:17.000000000 +0800
@@ -12,8 +12,10 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
-Configure: none
-Builder: none
+Builder: python
+
+Files:
+    - "%{python_sitelib}/*"
 
 SubPackages:
     - Name: devel
