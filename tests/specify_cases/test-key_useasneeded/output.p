--- output.orig.spec	2010-03-17 21:15:18.000000000 +0800
+++ output.spec	2010-03-17 21:15:19.000000000 +0800
@@ -38,6 +38,7 @@ This package contains development files 
 # << setup
 
 %build
+unset LD_AS_NEEDED
 # >> build pre
 # << build pre
 
