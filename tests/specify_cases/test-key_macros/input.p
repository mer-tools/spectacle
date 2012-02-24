--- ../base/testpkg.yaml	2011-09-30 10:44:02.158593700 +0300
+++ testpkg.yaml	2012-02-24 15:02:54.521492540 +0200
@@ -12,6 +12,9 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
+Macros:
+    - macros_key;macros_value
+
 Configure: none
 Builder: none
 
