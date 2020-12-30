#!/bin/bash

echo $PROJECT
if [[ -z "$PROJECT" ]]; then
	export PROJECT="GenPi64"
fi

if [[ -z "$PROJECT_DIR" ]]; then
	export PROJECT_DIR="${BASEDIR}/build/${PROJECT}"
fi

if [[ -z "$BINARY_ASSETS" ]]; then
	export BINARY_ASSETS="${PROJECT_DIR}/build-binary-assets"
fi

echo $PROJECT
#This list of variables must also be included in the copyenv directive of parsers/include
#export PROJECT_DIR="${BASEDIR}/build/${PROJECT}"
export CONFIG_DIR="${BASEDIR}/config"
export CHROOT_DIR="${PROJECT_DIR}/chroot"
export PARSERS="${BASEDIR}/parsers"
export SCRIPTS="${BASEDIR}/scripts"
export CALLBACKS="${BASEDIR}/callbacks"


cpu="$(uname -m)"
case "${cpu}" in
    armv[4-9]*)
	cpu="arm"
	;;
    i386|i486|i586|i686|i86pc|BePC)
	cpu="x86"
	;;
    mips*)
	cpu="mips"
	;;
    "Power Macintosh"|ppc|ppc64)
	cpu="ppc"
	;;
    s390*)
	cpu="s390"
	;;
    sh*)
	cpu="sh"
	;;
    sparc*)
	cpu="sparc"
	;;
esac

if [ "${cpu}" != "aarch64" ] ; then
    if [[ ! -e /proc/sys/fs/binfmt_misc/aarch64 ]]; then
	echo ":aarch64:M::\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\xB7\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/qemu-${cpu}-aarch64:" > /proc/sys/fs/binfmt_misc/register
    fi
fi

if [ "${cpu}" != "arm" ] ; then
    if [[ ! -e /proc/sys/fs/binfmt_misc/arm ]]; then
	echo ":arm:M::\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x28\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/qemu-${cpu}-arm:" > /proc/sys/fs/binfmt_misc/register
    fi
fi

