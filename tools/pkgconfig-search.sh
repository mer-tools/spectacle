#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <dir_to_devel_rpms>"
  exit 1
fi

DEVPKGS=`find $1 -name '*devel*.rpm'`

for DEVPKG in $DEVPKGS; do
  PKGCONFIGS=`rpm -qp --provides $DEVPKG | grep pkgconfig | cut -d ' ' -f -1`
  if [ -z "$PKGCONFIGS" ]; then
    continue
  fi

  DEVPKGNAME=`rpm -q --queryformat '%{NAME}' -p $DEVPKG`

  for PKGCONFIG in $PKGCONFIGS; do  
    echo "$DEVPKGNAME,$PKGCONFIG"
  done
done

