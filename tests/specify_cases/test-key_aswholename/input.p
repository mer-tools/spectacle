--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-15 16:21:22.000000000 +0800
@@ -16,7 +16,8 @@ Configure: none
 Builder: none
 
 SubPackages:
-    - Name: devel
+    - Name: haha-devel
+      AsWholeName: yes
       Summary: Development files for %{name}
       Group: Development/Libraries
       Description: This package contains development files for %{name}.
