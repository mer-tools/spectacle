--- output.orig.spec	2010-03-17 21:15:04.000000000 +0800
+++ output.spec	2010-03-17 21:15:04.000000000 +0800
@@ -41,7 +41,7 @@ This package contains development files 
 # >> build pre
 # << build pre
 
-
+%configure --disable-static
 
 # >> build post
 # << build post
