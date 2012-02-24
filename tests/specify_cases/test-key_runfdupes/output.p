--- output.orig.spec	2012-02-24 13:56:16.145406638 +0200
+++ output.spec	2012-02-24 13:56:16.315410467 +0200
@@ -16,6 +16,7 @@ License:    BSD
 URL:        http://www.testpkg.org/
 Source0:    http://www.testpkg.org/testpkg-%{version}.tar.gz
 Source100:  testpkg.yaml
+BuildRequires:  fdupes
 
 
 %description
@@ -57,6 +58,7 @@ rm -rf %{buildroot}
 # >> install post
 # << install post
 
+%fdupes  %{buildroot}/%{_datadir}
 
 %files
 %defattr(-,root,root,-)
