--- output.orig.spec	2010-03-30 19:59:59.000000000 +0800
+++ output.spec	2010-03-30 20:01:23.000000000 +0800
@@ -14,6 +14,9 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires(pre): GConf2
+Requires(preun): GConf2
+Requires(post): GConf2 >= 0.14
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -53,8 +56,26 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
-
-
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
 
 
 
@@ -63,6 +84,7 @@ rm -rf %{buildroot}
 
 %files
 %defattr(-,root,root,-)
+%{_libdir}/*.schema
 # >> files
 # << files
 
