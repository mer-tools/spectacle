16a17,18
> Requires(post): /sbin/install-info
> Requires(postun):  /sbin/install-info
57a60,61
> %post
> %install_info --info-dir=%_infodir %{_infodir}/*.info.gz
58a63,66
> %postun
> if [ $1 = 0 ] ;then
> %install_info_delete --info-dir=%{_infodir} %{_infodir}/*.info.gz
> fi
63a72
> %{_infodir}/*.info.gz
