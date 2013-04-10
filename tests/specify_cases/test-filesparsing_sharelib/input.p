--- ../base/testpkg.yaml	2012-07-06 23:03:05.000000000 +0000
+++ testpkg.yaml	2013-04-10 18:18:57.808090051 +0000
@@ -15,8 +15,21 @@ Description: |
 Configure: none
 Builder: none
 
+Files:
+    - "%{_libdir}/*.so"
+
 SubPackages:
+    - Name: subpkg
+      Summary: Development files for %{name}
+      Group: Development/Libraries
+      Description: This package contains development files for %{name}.
+      Files:
+          - "%{_libdir}/sub*.so"
+
     - Name: devel
       Summary: Development files for %{name}
       Group: Development/Libraries
       Description: This package contains development files for %{name}.
+      Files:
+          - "%{_libdir}/devel*.so"
+
