--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-30 20:01:22.000000000 +0800
@@ -14,6 +14,11 @@ Description: |
 
 Configure: none
 Builder: none
+RequiresPost:
+    - GConf2 >= 0.14
+
+Files:
+    - "%{_libdir}/*.schema"
 
 SubPackages:
     - Name: devel
