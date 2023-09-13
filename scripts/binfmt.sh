
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

if [ "${cpu}" != "aarch64" ] && [ -x /usr/bin/qemu-aarch64 ]; then
    if [[ ! -e /proc/sys/fs/binfmt_misc/aarch64 ]]; then
	echo ":aarch64:M::\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\xB7\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/qemu-aarch64:F" > /proc/sys/fs/binfmt_misc/register
    fi
fi

if [ "${cpu}" != "arm" ] && [ -x /usr/bin/qemu-arm ] ; then
    if [[ ! -e /proc/sys/fs/binfmt_misc/arm ]]; then
	echo ":arm:M::\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x28\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/qemu-arm:F" > /proc/sys/fs/binfmt_misc/register
    fi
fi

