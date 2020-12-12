#! /bin/bash

if [[ -z "$PROJECT" ]]; then
  PROJECT="gentoo-arm"
fi

BASEDIR=$( dirname $0 )

sudo pychroot -B "${BASEDIR}/build/${PROJECT}/packages":/usr/portage/packages  "${BASEDIR}/build/${PROJECT}/chroot"
