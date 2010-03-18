--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-18 16:04:23.000000000 +0800
@@ -14,6 +14,9 @@ Description: |
 
 Configure: none
 Builder: none
+PkgBR:
+    - intltool
+NoAutoLocale: yes
 
 SubPackages:
     - Name: devel
