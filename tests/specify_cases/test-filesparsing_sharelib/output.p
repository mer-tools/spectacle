16a17,18
> Requires(post):  /sbin/ldconfig
> Requires(postun):  /sbin/ldconfig
57a60
> %post -p /sbin/ldconfig
58a62
> %postun -p /sbin/ldconfig
63a68
> %{_libdir}/*.so
