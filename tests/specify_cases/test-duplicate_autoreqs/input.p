--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-30 19:58:43.000000000 +0800
@@ -14,6 +14,10 @@ Description: |
 
 Configure: none
 Builder: none
+RequiresPost: /sbin/ldconfig
+RequiresPostUn: /sbin/ldconfig
+Files:
+    - "%{_libdir}/*.so"
 
 SubPackages:
     - Name: devel
