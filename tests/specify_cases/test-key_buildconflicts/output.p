--- output.orig.spec	2010-06-21 16:34:07.000000000 +0800
+++ output.spec	2010-06-21 16:34:38.000000000 +0800
@@ -14,6 +14,8 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildConflicts: package-conflict1
+BuildConflicts: package-conflict2
 
 
 %description
