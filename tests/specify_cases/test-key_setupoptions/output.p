--- output.orig.spec	2010-03-17 21:15:12.000000000 +0800
+++ output.spec	2010-03-17 21:15:13.000000000 +0800
@@ -32,7 +32,7 @@ This package contains development files 
 
 
 %prep
-%setup -q -n %{name}-%{version}
+%setup --setup-opt-sample
 
 # >> setup
 # << setup
