--- ../base/testpkg.yaml	2010-09-07 11:40:02.000000000 +0800
+++ testpkg.yaml	2011-06-20 17:10:16.695491164 +0800
@@ -15,8 +15,13 @@ Description: |
 Configure: none
 Builder: none
 
+Files:
+    - "/%{_lib}/systemd/system/abc.service"
+
 SubPackages:
     - Name: devel
       Summary: Development files for %{name}
       Group: Development/Libraries
       Description: This package contains development files for %{name}.
+      Files:
+          - "/lib/systemd/system/xyz.service"
