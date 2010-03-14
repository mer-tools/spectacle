--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-10 23:54:19.000000000 +0800
@@ -14,6 +14,9 @@ Description: |
 
 Configure: none
 Builder: none
+Files:
+    - "%doc README INST"
+    - "%{_bindir}/*"
 
 SubPackages:
     - Name: devel
