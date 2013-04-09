--- ../base/testpkg.yaml	2012-07-06 23:03:05.000000000 +0000
+++ testpkg.yaml	2013-04-09 05:27:50.640454464 +0000
@@ -14,9 +14,16 @@ Description: |
 
 Configure: none
 Builder: none
+NoAutoReq: yes
+NoAutoProv: yes
+NoAutoReqProv: yes
 
 SubPackages:
     - Name: devel
       Summary: Development files for %{name}
       Group: Development/Libraries
       Description: This package contains development files for %{name}.
+      NoAutoReq: yes
+      NoAutoProv: yes
+      NoAutoReqProv: yes
+
