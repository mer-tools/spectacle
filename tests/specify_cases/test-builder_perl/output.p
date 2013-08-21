--- output.orig.spec	2010-03-17 21:15:02.000000000 +0800
+++ output.spec	2010-03-17 21:15:02.000000000 +0800
@@ -14,6 +14,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
 
 %description
 Sample package for spectacle testings, which will be used as
@@ -41,7 +42,13 @@ This package contains development files 
 # >> build pre
 # << build pre
 
-
+if test -f Makefile.PL; then
+%{__perl} Makefile.PL INSTALLDIRS=vendor
+make %{?_smp_mflags}
+else
+%{__perl} Build.PL  --installdirs vendor
+./Build
+fi
 
 # >> build post
 # << build post
@@ -49,6 +56,15 @@ This package contains development files 
 rm -rf %{buildroot}
 # >> install pre
 # << install pre
+if test -f Makefile.PL; then
+make pure_install PERL_INSTALL_ROOT=%{buildroot}
+else
+./Build install --installdirs vendor
+fi
+find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
+find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
+find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
+%{_fixperms} %{buildroot}/*
 
 # >> install post
 # << install post
