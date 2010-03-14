43a44,45
> %configure --disable-static \
>     --otheropt
44a47
> make %{?jobs:-j%jobs}
51a55
> %make_install
