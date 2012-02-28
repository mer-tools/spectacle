--- output.orig.spec	2012-02-28 09:40:01.801473292 +0200
+++ output.spec	2012-02-28 09:40:22.710930552 +0200
@@ -24,12 +24,36 @@ specified, plus with one sub package "de
 
 
 %package devel
-Summary:    Development files for %{name}
+Summary:    Development files for %{name}.
 Group:      Development/Libraries
 Requires:   %{name} = %{version}-%{release}
 
 %description devel
-This package contains development files for %{name}.
+Development files for %{name}
+
+%package docs
+Summary:    Documentation files for %{name}.
+Group:      Development/Libraries
+Requires:   %{name} = %{version}-%{release}
+
+%description docs
+Documentation files for %{name}
+
+%package lang
+Summary:    Translation files for %{name}.
+Group:      Development/Libraries
+Requires:   %{name} = %{version}-%{release}
+
+%description lang
+Translation files for %{name}
+
+%package abc
+Summary:    Files for %{name}.
+Group:      Development/Libraries
+Requires:   %{name} = %{version}-%{release}
+
+%description abc
+Files for %{name}
 
 
 %prep
@@ -65,3 +89,18 @@ rm -rf %{buildroot}
 %defattr(-,root,root,-)
 # >> files devel
 # << files devel
+
+%files docs
+%defattr(-,root,root,-)
+# >> files docs
+# << files docs
+
+%files lang
+%defattr(-,root,root,-)
+# >> files lang
+# << files lang
+
+%files abc
+%defattr(-,root,root,-)
+# >> files abc
+# << files abc
