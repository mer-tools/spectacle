6a7
> %define keepstatic 1
44c45,46
< 
---
> %configure 
> make %{?jobs:-j%jobs}
51a54
> %make_install
64a68
> %{_libdir}/*.a
