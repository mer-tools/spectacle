16a17,18
> Requires(post):  /sbin/ldconfig
> Requires(postun):  /sbin/ldconfig
58a61
> %post -p /sbin/ldconfig
59a63
> %postun -p /sbin/ldconfig
64a69
> %{_libdir}/*.so
