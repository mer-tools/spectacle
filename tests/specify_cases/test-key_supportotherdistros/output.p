7a8
> %{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
44c45
< 
---
> CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
51a53,57
> %if 0%{?suse_version}
> %{__python} setup.py install --root=%{buildroot} --prefix=%{_prefix}
> %else
> %{__python} setup.py install --root=%{buildroot} -O1
> %endif
