--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-14 15:57:04.000000000 +0800
@@ -19,4 +19,6 @@ SubPackages:
     - Name: devel
       Summary: Development files for %{name}
       Group: Development/Libraries
+      Requires:
+          - "%{name} = %{version}-%{release}"  
       Description: This package contains development files for %{name}.
