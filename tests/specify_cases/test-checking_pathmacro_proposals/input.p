--- ../base/testpkg.yaml	2010-09-07 11:40:02.000000000 +0800
+++ testpkg.yaml	2011-06-20 17:06:35.749534033 +0800
@@ -15,6 +15,12 @@ Description: |
 Configure: none
 Builder: none
 
+Files:
+    - /usr/bin/abc
+    - /usr/share/info/info.gz
+    - /usr/share/testpkg/api
+
+
 SubPackages:
     - Name: devel
       Summary: Development files for %{name}
