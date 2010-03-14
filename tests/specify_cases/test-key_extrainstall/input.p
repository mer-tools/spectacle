--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-14 23:09:33.000000000 +0800
@@ -14,6 +14,9 @@ Description: |
 
 Configure: none
 Builder: none
+ExtraInstall: |
+    # extra install scripts in %install
+    # etc.
 
 SubPackages:
     - Name: devel
