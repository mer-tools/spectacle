--- output.orig.spec	2012-02-24 15:01:25.458498103 +0200
+++ output.spec	2012-02-24 15:01:51.080071835 +0200
@@ -34,6 +34,8 @@ Requires:   %{name} = %{version}-%{relea
 This package contains development files for %{name}.
 
 
+%define macros2_key macros2_value
+
 %prep
 %setup -q -n %{name}-%{version}
 
