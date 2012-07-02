--- ../base/testpkg.yaml	2012-06-25 14:18:41.048150783 +0300
+++ testpkg.yaml	2012-07-02 15:12:12.869536868 +0300
@@ -12,11 +12,15 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
+PkgBR:
+    - intltool
+
 Configure: none
 Builder: none
+LocaleFilesPkgName: mylocale
 
 SubPackages:
-    - Name: devel
-      Summary: Development files for %{name}
+    - Name: mylocale
+      Summary: My locale files for %{name}
       Group: Development/Libraries
-      Description: This package contains development files for %{name}.
+      Description: This package contains locale files for %{name}.
