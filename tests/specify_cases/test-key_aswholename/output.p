--- output.orig.spec	2010-03-17 21:15:08.000000000 +0800
+++ output.spec	2010-03-17 21:15:09.000000000 +0800
@@ -22,12 +22,12 @@ specified, plus with one sub package "de
 
 
 
-%package devel
+%package -n haha-devel
 Summary:    Development files for %{name}
 Group:      Development/Libraries
 Requires:   %{name} = %{version}-%{release}
 
-%description devel
+%description -n haha-devel
 This package contains development files for %{name}.
 
 
@@ -65,8 +65,8 @@ rm -rf %{buildroot}
 # << files
 
 
-%files devel
+%files -n haha-devel
 %defattr(-,root,root,-)
-# >> files devel
-# << files devel
+# >> files haha-devel
+# << files haha-devel
 
