--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-15 15:47:50.000000000 +0800
@@ -14,6 +14,11 @@ Description: |
 
 Configure: none
 Builder: none
+Documents:
+    - README
+    - DOC
+PostScripts: |
+    # scripts in %post
 
 SubPackages:
     - Name: devel
