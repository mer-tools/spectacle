--- output.orig.spec	2010-03-17 21:15:03.000000000 +0800
+++ output.spec	2010-03-17 21:15:03.000000000 +0800
@@ -41,7 +41,8 @@ This package contains development files 
 # >> build pre
 # << build pre
 
-
+%configure --disable-static
+make
 
 # >> build post
 # << build post
@@ -49,6 +50,7 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+%make_install
 
 # >> install post
 # << install post
