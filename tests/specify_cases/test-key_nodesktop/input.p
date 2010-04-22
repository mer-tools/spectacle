--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-04-22 19:12:36.000000000 +0800
@@ -14,6 +14,9 @@ Description: |
 
 Configure: none
 Builder: none
+NoDesktop: yes
+Files:
+    - "%{_datadir}/*.desktop"
 
 SubPackages:
     - Name: devel
