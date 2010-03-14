--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-14 17:45:02.000000000 +0800
@@ -14,6 +14,9 @@ Description: |
 
 Configure: none
 Builder: none
+PostScripts: |
+    #do more stuff in %install post
+    # etc.
 
 SubPackages:
     - Name: devel
