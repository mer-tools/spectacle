--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-14 15:06:15.000000000 +0800
@@ -12,6 +12,8 @@ Description: |
     the base of all testings. In this YAML file, only basic keywords
     specified, plus with one sub package "devel".
 
+NoAutoReq: yes
+NoAutoProv: yes
 Configure: none
 Builder: none
 
