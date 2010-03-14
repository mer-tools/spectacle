--- ../base/testpkg.yaml	2010-03-09 17:48:35.000000000 +0800
+++ testpkg.yaml	2010-03-10 23:53:57.000000000 +0800
@@ -4,6 +4,7 @@ Version: 1.0
 Release: 1
 Group: System/Base
 License: BSD
+ExclusiveArch: amd64
 URL: http://www.testpkg.org/
 Sources:
     - http://www.testpkg.org/testpkg-%{version}.tar.gz
