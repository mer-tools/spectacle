--- output.orig.spec	2013-04-10 18:02:07.130456608 +0000
+++ output.spec	2013-04-10 18:02:13.509504783 +0000
@@ -26,7 +26,6 @@ specified, plus with one sub package "de
 %package devel
 Summary:    Development files for %{name}
 Group:      Development/Libraries
-Requires:   %{name} = %{version}-%{release}
 
 %description devel
 This package contains development files for %{name}.
@@ -54,10 +53,6 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
-%files
-%defattr(-,root,root,-)
-# >> files
-# << files
 
 %files devel
 %defattr(-,root,root,-)
