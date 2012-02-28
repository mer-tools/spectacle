--- ../base/testpkg.yaml	2011-09-30 10:44:02.158593700 +0300
+++ testpkg.yaml	2012-02-28 09:40:22.537926773 +0200
@@ -15,8 +15,9 @@ Description: |
 Configure: none
 Builder: none
 
-SubPackages:
-    - Name: devel
-      Summary: Development files for %{name}
-      Group: Development/Libraries
-      Description: This package contains development files for %{name}.
+AutoSubPackages:
+    - devel
+    - docs
+    - lang
+    - abc
+
