--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-14 17:49:28.000000000 +0800
@@ -14,6 +14,8 @@ Description: |
 
 Configure: none
 Builder: none
+Files:
+    - "%{_infodir}/*.info.gz"
 
 SubPackages:
     - Name: devel
