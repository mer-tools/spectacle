--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-14 16:06:04.000000000 +0800
@@ -14,6 +14,9 @@ Description: |
 
 Configure: none
 Builder: none
+Files:
+    - "%defattr(-,root,root,-)"
+    - "%{_bindir}/*"
 
 SubPackages:
     - Name: devel
