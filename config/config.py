import os
import uuid

if os.path.exists(p := os.path.join(os.environ['PROJECT_DIR'], 'uuid')):
    with open(p) as f:
        UUID = f.read()
else:
    UUID = str(uuid.uuid4())
    with open(p, 'w') as f:
        f.write(UUID)


def readlines(p):
    with open(p) as f:
        return (i.split('#', 1)[0].strip() for i in f.read().split('\n'))


Base = {
    'portage': {
        "make.conf": dict(
            CFLAGS="-march=native -O2 -pipe",
            CXXFLAGS="${CFLAGS}",
            FCFLAGS="${CFLAGS}",
            FFLAGS="${CFLAGS}",
            CHOST="aarch64-unknown-linux-gnu",
            USE="bindist -systemd elogind".split(),
            FEATURES="parallel-fetch parallel-install buildpkg binpkg-multi-instance getbinpkg ".split(),
            MAKEOPTS=f"-j{len(os.sched_getaffinity(0))} -l{len(os.sched_getaffinity(0))}",
            VIDEO_CARDS="",
            INPUT_DEVICES="evdev synaptics",
        ),
        "patches/": {
            "app-editors/": "patches/app-editors",
            "sys-apps/": "patches/sys-apps"
        },
        "savedconfig/": {
            "sys-kernel/": {
                "linux-firmware": "linux-firmware"
            }
        },
        "env/": {
            "enable-distcc": ['FEATURES="${FEATURES} distcc"']
        },
        "package.env/": {
            "distcc": [[pn, " enable-distcc"] for pn in
                       readlines(os.path.join(os.environ.get('CONFIG_DIR'), 'distcc-pkgs')) if pn]
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
        "rsyslog": "default",
        "chronyd": "default",
        "rngd": "boot",
        "rpi3-ondemand": "default"
    },
    'sets': [
        "standard"
    ],
    'packages': []
}

GenPi64 = Base | {
    "cmdline": 'console=serial0,115200 console=tty1 dwc_otg.lpm_enable=0 root=PARTUUID=%(UUID)s rootfstype=%(fstype)s elevator=deadline fsck.repair=no usbhid.mousepoll=0 rootwait',
    "kernel": [
        "sys-firmware/raspberrypi-wifi-ucode",
        "sys-kernel/linux-firmware",
        "sys-kernel/raspberrypi-kernel",
        "sys-boot/raspberrypi-firmware"
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
            'sync-git-clone-extra-opts': '--single-branch --branch master'
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
            "FEATURES": Base["portage"]["make.conf"][
                            "FEATURES"] + "-userpriv -usersandbox -network-sandbox -pid-sandbox".split(),
            "USE": Base["portage"]["make.conf"]["USE"] + ["-checkboot"]
        },
        "binrepos.conf": [
            "[genpi64-binhost]",
            "priority = 9999",
            "sync-uri = https://packages.genpi64.com/",
            "",
            "[genpi64-european-binhost]",
            "priority = 9998",
            "sync-uri = https://fi.packages.genpi64.com/"
        ],
        "package.mask": "package.mask"
    },
    "etc": Base["etc"] | {
        "kernel/": {
            "config.d/": {
                i: "kernel-config/" + i for i in os.listdir(os.path.join(os.environ.get('CONFIG_DIR'), 'kernel-config'))
            }
        }
    },
    "stage3": os.environ.get("STAGE3", "stage3-arm64.tar.xz"),
    "stage3url": "http://distfiles.gentoo.org/releases/arm64/autobuilds/latest-stage3-arm64.txt",
    "stage3mirror": "http://distfiles.gentoo.org/releases/arm64/autobuilds/",
    "profile": "genpi64:default/linux/arm64/17.0/genpi64",
    'users': [
        Base['users'][0] | dict(
            password="raspberrypi64",
            groups=Base['users'][0]['groups'] + ['plugdev', 'gpio', 'i2c', 'spi']
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
        'mount-order': [1, 0],
        'uuid': UUID[:8],
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
                'mount-options': 'noatime,compress=zstd:15,ssd,discard',
                'args': f'--force'
            }
        ]
    }
}

GenPi64Desktop = GenPi64 | {
    "profile": "genpi64:default/linux/arm64/17.0/genpi64/desktop",
    'sets': GenPi64['sets'] + ['pi4desktop'],
    'image': GenPi64['image'] | {
        'name': 'GenPi64Desktop.img'
    }
}

GenPi32 = GenPi64 | {
    "stage3": "stage3-armv6j_hardfp.tar.xz",
    "stage3url": "http://distfiles.gentoo.org/releases/arm/autobuilds/latest-stage3-armv6j_hardfp.txt",
    "stage3mirror": "http://distfiles.gentoo.org/releases/arm/autobuilds/",
    "portage": GenPi64['portage'] | {
        "make.conf": GenPi64['portage']['make.conf'] | {
            "CFLAGS": "-O2 -pipe -march=armv6j -mfpu=vfp -mfloat-abi=hard -fomit-frame-pointer -fno-stack-protector",
            "CHOST": "armv6j-unknown-linux-gnueabihf"
        }
    },
    "profile": "default/linux/arm/17.0"
}

GentooAMD64 = Base | {
    "stage3": "stage3-amd64.tar.xz",
    "stage3url": "http://distfiles.gentoo.org/releases/amd64/autobuilds/latest-stage3-amd64.txt",
    "stage3mirror": "http://distfiles.gentoo.org/releases/amd64/autobuilds/",
    "profile": "default/linux/amd64/17.1",
    'sets': Base['sets'] + ['amd64'],
    'portage': Base['portage'] | {
        "make.conf": Base['portage']['make.conf'] | {
            'CHOST': 'x86_64-unknown-linux-gnu',
            'USE': Base['portage']['make.conf']['USE'] + 'openssl'.split(),
            'GRUB_PLATFORMS': "efi-64",
        },
        "package.license": [
            "# required by sys-kernel/linux-firmware (argument)",
            "=sys-kernel/linux-firmware-20201218 linux-fw-redistributable no-source-code"
        ],
        "env/": {},
        "package.env/": {},
        "package.use/": {
            "elogind": [
                "# Required so it does not pull in spidermonkey",
                "sys-auth/elogind -policykit"
            ],
        },
    },
    "kernel": [
        "sys-kernel/gentoo-kernel",
        "sys-kernel/linux-firmware"
    ],
    "etc": Base["etc"] | {
        "kernel/": {
            "config.d/": {
                i: "kernel-config/" + i for i in os.listdir(os.path.join(os.environ.get('CONFIG_DIR'), 'kernel-config'))
            }
        }
    },
    "services": {
        "cronie": "default",
        "sshd": "default",
        "elogind": "default",
        "rsyslog": "default",
        "chronyd": "default",
        "rngd": "boot"
    },
    'image': GenPi64['image'] | {
        'name': 'GentooAMD64Server.img',
        'format': 'gpt',
        'partitions': [
            GenPi64['image']['partitions'][0] | {
                'flags': {
                    'boot': 'on'
                }
            },
            GenPi64['image']['partitions'][1] | {
                'uuid': UUID
            }
        ]
    }
}
