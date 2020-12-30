import os
import uuid

if os.path.exists(p:=os.path.join(os.environ['PROJECT_DIR'], 'uuid')):
    with open(p) as f:
        UUID = f.read()
else:
    UUID=str(uuid.uuid4())[:8]
    with open(p, 'w') as f:
        f.write(UUID)

Base = {
    'portage': {
        "make.conf": dict(
            CFLAGS="-march=native -O2 -pipe",
            CXXFLAGS="${CFLAGS}",
            FCFLAGS="${CFLAGS}",
            FFLAGS="${CFLAGS}",
            CHOST="aarch64-unknown-linux-gnu",
            USE="bindist -systemd elogind".split(),
            FEATURES="parallel-fetch distcc parallel-install buildpkg binpkg-multi-instance getbinpkg ".split(),
            MAKEOPTS=f"-j{len(os.sched_getaffinity(0))} -l{len(os.sched_getaffinity(0))}",
            VIDEO_CARDS="",
            INPUT_DEVICES="evdev synaptics",
            ACCEPT_LICENSE="* -@EULA",
            LINGUAS="en",
            L10N="en",
        ),
        "patches/": {
            "app-editors/": "patches/app-editors",
            "sys-apps/": "patches/sys-apps"
        }
    },
    "etc": {
        "locale.gen": "locale.gen",
        "profile": "profile"
    },
    "TERM": os.environ['TERM'],
    "jobs": len(os.sched_getaffinity(0)),
    "load-average": len(os.sched_getaffinity(0)),
    "distcc": [
        os.environ.get("DISTCC_HOSTS", "")
    ],
    "groups": [
        dict(name="cron", gid=16),
    ],
    "users": [
        dict(name="demouser",
             password="password",
             format="SHA512",
             group="users",
             groups="users,wheel,video,audio,adm,disk,lp,cdrom,usb,portage,cron".split(','),
             shell="/bin/bash",
             uid="1000"
        )
    ],
    "locale": "en_US.utf8",
    "overlays": [
        {
            'name': 'gentoo',
            'location': '/var/db/repos/gentoo',
            'sync-type': 'git',
            'clone-depth': '1',
            'sync-depth': '1',
            'sync-uri': 'https://github.com/gentoo-mirror/gentoo',
            'auto-sync': 'yes',
            'sync-git-verify-commit-signature': 'true'
        }
    ],
    "services": {
        "cronie": "default",
        "sshd": "default",
        "elogind": "default",
        "ntp-client": "default"
    },
    'sets': [
        "standard"
    ],
    'packages': []
}

GenPi64 = Base | {
    "cmdline": 'dwc_otg.lpm_enable=0 root=PARTUUID=%(UUID)s rootfstype=%(fstype)s elevator=deadline fsck.repair=no usbhid.mousepoll=0 rootwait',
    "kernel": [
        "sys-kernel/bcm2711-kernel-bis-bin",
        "sys-boot/rpi3-64bit-firmware"
    ],
    "overlays": Base['overlays'] + [
        {
            'name': 'genpi64',
            'location': '/var/db/repos/genpi64',
            'sync-type': 'git',
            'sync-uri': 'https://github.com/GenPi64/genpi64-overlay.git',
            'priority': '100',
            'auto-sync': 'yes',
            'clone-depth': '1',
            'sync-depth': '1',
            'sync-git-clone-extra-opts': '--single-branch --branch alpha4'
        },
        {
            'name': 'genpi-tools',
            'location': '/var/db/repos/sakaki-tools',
            'sync-type': 'git',
            'sync-uri': 'https://github.com/GenPi64/sakaki-tools.git',
            'priority': '50',
            'auto-sync': 'yes',
            'clone-depth': '1',
            'sync-depth': '1',
        }
    ],
    "portage": Base["portage"] | {
        "make.conf": Base["portage"]["make.conf"] | {
            "CFLAGS": "-mtune=cortex-a72 -march=armv8-a+crc -O2 -pipe",
            "PORTAGE_BINHOST": "https://genpi64.com/",
            "FEATURES": Base["portage"]["make.conf"]["FEATURES"] + "-userpriv -usersandbox -network-sandbox -pid-sandbox".split(),
            "USE": Base["portage"]["make.conf"]["USE"] + ["-checkboot"]
        },
        "binrepos.conf": "binrepo_genpi64.conf",
        "package.mask": "package.mask"
    },
    "stage3": os.environ.get("STAGE3", "stage3-arm64.tar.xz"),
    "stage3url": "http://distfiles.gentoo.org/releases/arm64/autobuilds/latest-stage3-arm64.txt",
    "stage3mirror": "http://distfiles.gentoo.org/releases/arm64/autobuilds/",
    "profile": "genpi64:default/linux/arm64/17.0/desktop/genpi64",
    'users': [
        dict(name="demouser",
             password="raspberrypi64",
             format="SHA512",
             group="100",
             groups="users,wheel,video,audio,adm,disk,lp,cdrom,usb,portage,cron,plugdev,gpio,i2c,spi".split(','),
             shell="/bin/bash",
             uid="1000"
        )
    ],

    'groups': [
        dict(name="i2c", gid=371),
        dict(name="gpio", gid=370),
        dict(name="spi", gid=372),
        dict(name="cron", gid=16),
        dict(name="crontab", gid=248),
        dict(name="plugdev", gid=245),
    ],

    'sets': Base['sets'] + ['pi4'],
    'image': {
        'name': 'GenPi64.img',
        'size': '8G',
        'format': 'msdos',
        'mount-order': [1,0],
        'uuid': UUID,
        'partitions': [
            {
                'end': '256MiB',
                'format': 'vfat',
                'mount-point': '/boot',
                'mount-options': 'noatime',
                'flags': {
                    'lba': 'on'
                }
            },
            {
                'end': '100%',
                'format': 'btrfs',
                'mount-point': '/',
                'mount-options': 'compress=zstd:15,ssd,discard',
                'args': f'--force'
            }
        ]
    }
}

GenPi64Desktop = GenPi64 | {
    "profile": "genpi64:default/linux/arm64/17.0/desktop/genpi64",
    'sets': GenPi64['sets'] + ['pi4desktop'],
    'image': GenPi64['image'] | {
        'name': 'GenPi64Desktop.img'
    }
}


GentooAMD64 = Base | {
    # stuff
}

GenPi32 = GenPi64 | {
    "stage3": "stage3-armv6j_hardfp.tar.xz",
    "stage3url": "http://distfiles.gentoo.org/releases/arm/autobuilds/latest-stage3-armv6j_hardfp.txt",
    "stage3mirror": "http://distfiles.gentoo.org/releases/arm/autobuilds/",
    "portage": GenPi64['portage'] | {
        "make.conf": GenPi64['portage']['make.conf'] | {
            "CFLAGS": "-O2 -pipe -march=armv6j -mfpu=vfp -mfloat-abi=hard -fomit-frame-pointer -fno-stack-protector",
            "CHOST":"armv6j-unknown-linux-gnueabihf"
        }
    },
    "profile": "default/linux/arm/17.0"
}
