16a17
> BuildRequires: desktop-file-utils
54a56,58
> desktop-file-install --delete-original       \
>   --dir %{buildroot}%{_datadir}/applications             \
>    %{buildroot}%{_datadir}/applications/*
63a68
> %{_datadir}/*.desktop
