16a17,18
> Requires(post): /sbin/install-info
> Requires(postun):  /sbin/install-info
58a61,62
> %post
> %install_info --info-dir=%_infodir %{_infodir}/*.info.gz
59a64,67
> %postun
> if [ $1 = 0 ] ;then
> %install_info_delete --info-dir=%{_infodir} %{_infodir}/*.info.gz
> fi
64a73
> %{_infodir}/*.info.gz
