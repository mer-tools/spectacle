--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-06-21 16:34:38.000000000 +0800
@@ -12,6 +12,10 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
+BuildConflicts:
+    - package-conflict1
+    - package-conflict2
+
 Configure: none
 Builder: none
 
