--- ../base/testpkg.yaml	2010-09-07 11:40:02.000000000 +0800
+++ testpkg.yaml	2011-06-20 16:50:04.845494495 +0800
@@ -15,6 +15,11 @@ Description: |
 Configure: none
 Builder: none
 
+Files:
+    - arm:%{_bin}/testpkg-arm
+    - ix86:%{_bin}/testpkg-ix86
+    - "%{_bin}/testpkg"
+
 SubPackages:
     - Name: devel
       Summary: Development files for %{name}
