--- output.orig.spec	2012-02-24 13:53:30.253671931 +0200
+++ output.spec	2012-02-24 13:53:30.430675915 +0200
@@ -25,12 +25,12 @@ specified, plus with one sub package "de
 
 
 
-%package devel
+%package -n haha-devel
 Summary:    Development files for %{name}
 Group:      Development/Libraries
 Requires:   %{name} = %{version}-%{release}
 
-%description devel
+%description -n haha-devel
 This package contains development files for %{name}.
 
 
@@ -63,7 +63,7 @@ rm -rf %{buildroot}
 # >> files
 # << files
 
-%files devel
+%files -n haha-devel
 %defattr(-,root,root,-)
-# >> files devel
-# << files devel
+# >> files haha-devel
+# << files haha-devel
