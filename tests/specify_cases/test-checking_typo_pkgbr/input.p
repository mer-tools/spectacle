--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-07-23 11:20:04.151422059 +0800
@@ -15,6 +15,9 @@ Description: |
 Configure: none
 Builder: none
 
+BuildRequires:
+    - abc
+
 SubPackages:
     - Name: devel
       Summary: Development files for %{name}
