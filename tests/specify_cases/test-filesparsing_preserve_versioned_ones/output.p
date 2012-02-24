--- output.orig.spec	2012-02-24 13:49:53.522792704 +0200
+++ output.spec	2012-02-24 13:49:53.697796645 +0200
@@ -16,6 +16,10 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(pre): %{_bindir}/gconftool-2
+Requires(preun): %{_bindir}/gconftool-2
+Requires(post): GConf2 >= 0.14
+Requires(post): %{_bindir}/gconftool-2
 
 
 %description
@@ -58,8 +62,30 @@ rm -rf %{buildroot}
 # << install post
 
 
+%pre
+if [ "$1" -gt 1 ]; then
+  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
+  gconftool-2 --makefile-uninstall-rule \
+    %{_libdir}/*.schema \
+    > /dev/null || :
+fi
+
+%preun
+if [ "$1" -eq 0 ]; then
+  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
+  gconftool-2 --makefile-uninstall-rule \
+    %{_libdir}/*.schema \
+    > /dev/null || :
+fi
+
+%post
+export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
+gconftool-2 --makefile-install-rule \
+    %{_libdir}/*.schema  > /dev/null || :
+
 %files
 %defattr(-,root,root,-)
+%{_libdir}/*.schema
 # >> files
 # << files
 
