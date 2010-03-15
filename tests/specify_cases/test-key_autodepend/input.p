--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-15 16:15:18.000000000 +0800
@@ -17,6 +17,7 @@ Builder: none
 
 SubPackages:
     - Name: devel
+      AutoDepend: no
       Summary: Development files for %{name}
       Group: Development/Libraries
       Description: This package contains development files for %{name}.
