--- ../base/testpkg.yaml	2010-03-15 12:26:52.000000000 +0800
+++ testpkg.yaml	2010-03-31 17:20:07.000000000 +0800
@@ -12,6 +12,9 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
+SetupOptions: -q -n xyz
+SourcePrefix: xyz
+
 Configure: none
 Builder: none
 
