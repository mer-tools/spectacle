16a17
> Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
44c45,51
< 
---
> if test -f Makefile.PL; then
> %{__perl} Makefile.PL INSTALLDIRS=vendor
> make %{?jobs:-j%jobs}
> else
> %{__perl} Build.PL  --installdirs vendor
> ./Build
> fi
51a59,67
> if test -f Makefile.PL; then
> make pure_install PERL_INSTALL_ROOT=%{buildroot}
> else
> ./Build install --installdirs vendor
> fi
> find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
> find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
> find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
> %{_fixperms} %{buildroot}/*
