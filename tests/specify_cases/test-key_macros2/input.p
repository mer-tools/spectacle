--- ../base/testpkg.yaml	2011-09-30 10:44:02.158593700 +0300
+++ testpkg.yaml	2012-02-24 15:01:50.909068078 +0200
@@ -12,6 +12,9 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
+Macros2:
+    - macros2_key;macros2_value
+
 Configure: none
 Builder: none
 
