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
            USE=["bindist"],
            FEATURES="parallel-fetch parallel-install ".split(),
            MAKEOPTS=f"-j{len(os.sched_getaffinity(0))} -l{len(os.sched_getaffinity(0))}",
            VIDEO_CARDS="",
            INPUT_DEVICES="evdev synaptics"
        ),
        "patches/": {
            "app-editors/": "patches/app-editors",
            "sys-apps/": "patches/sys-apps",
            "dev-lang/": "patches/dev-lang"
        },
        "savedconfig/": {
            "sys-kernel/": {
                "linux-firmware": "linux-firmware"
            }
        },
        "env/": {
            "enable-distcc": ['FEATURES="${FEATURES} distcc"'],
            "dev-lang/": { "python": "patches/python-env" }
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
            'sync-git-verify-commit-signature': 'true',
            "#commit-hash": "HEAD",
            "#clone-date": "2021-08-23",

        }
    ],
    'sets': [],
    'packages': []
}

GenPi64Generic = Base | {
    "stage3": os.environ.get("STAGE3", "stage3-arm64.tar.xz"),
    "stage3url": "http://distfiles.gentoo.org/releases/arm64/autobuilds/latest-stage3-arm64.txt",
    "stage3mirror": "http://distfiles.gentoo.org/releases/arm64/autobuilds/",
    "profile": "default/linux/arm64/17.0",
    "kernel": [
        "sys-kernel/gentoo-kernel-bin"
    ],
    'portage': {
        "make.conf": dict(
            CFLAGS="-mtune=generic -O2 -pipe",
            CXXFLAGS="${CFLAGS}",
            FCFLAGS="${CFLAGS}",
            FFLAGS="${CFLAGS}",
            USE=["bindist"],
            FEATURES="parallel-fetch parallel-install -userpriv -usersandbox -network-sandbox -pid-sandbox".split(),
            MAKEOPTS=f"-j{len(os.sched_getaffinity(0))} -l{len(os.sched_getaffinity(0))}",
            VIDEO_CARDS=""

        ),
        "patches/": {},
        "savedconfig/": {
            "sys-kernel/": {
                "linux-firmware": "linux-firmware"
            }
        },
        "env/": {},
        "package.env/": {}
    },
    'groups': [
        dict(name="cron", gid=16),
        dict(name="crontab", gid=248),
        dict(name="plugdev", gid=245),
    ],
    'image': {
        'name': 'GenPi64Generic.img',
        'size': '8G',
        'format': 'gpt',
        'mount-order': [2, 1, 0],
        'uuid': UUID[:8],
        'partitions': [
            {
                'end': '100MiB',
                'format': 'vfat',
                'mount-point': '/boot/efi',
                'mount-options': 'noatime',
                'flags': {
                    'boot': 'on'
                }
            },
            {
              'end': '500MiB',
              'format': 'vfat',
              'mount-point': '/boot',
              'mount-options': 'noatime'
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

GenPi64 = Base | {
    "cmdline": 'console=serial0,115200 console=tty1 dwc_otg.lpm_enable=0 root=PARTUUID=%(PARTUUID)s rootfstype=%(fstype)s fsck.repair=no usbhid.mousepoll=0 rootwait=10 init=/sbin/init',
    "kernel": [
        "sys-firmware/raspberrypi-wifi-ucode",
        "sys-kernel/raspberrypi-kernel",
        "sys-boot/raspberrypi-firmware",
        "sys-kernel/raspberrypi-initramfs"
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
            'sync-git-clone-extra-opts': '--single-branch --branch alpha9',
            "#commit-hash": "HEAD",
            "#clone-date": "2021-08-24"
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
            "#commit-hash": "HEAD",
            "#clone-date": "2021-01-01"
        }
    ],
    "portage": Base["portage"] | {
        "make.conf": Base["portage"]["make.conf"] | {
            "CFLAGS": "-mtune=cortex-a72 -march=armv8-a+crc -O2 -pipe",
            'CC':"aarch64-unknown-linux-gnu-gcc-10.3.0",
            'CXX':"aarch64-unknown-linux-gnu-g++-10.3.0",
            'CHOST':"aarch64-unknown-linux-gnu",
            "FEATURES": Base["portage"]["make.conf"][
                            "FEATURES"] + "-userpriv -usersandbox -network-sandbox -pid-sandbox".split(),
            "USE": Base["portage"]["make.conf"]["USE"] + ["-checkboot"],
            "VIDEO_CARDS": ["vc4"] + ["v3d"] + ["fbdev"]
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
        "package.mask": "package.mask",
        "package.accept_keywords": "package.accept_keywords"
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

    'image': {
        'name': 'GenPi64.img',
        'size': '8G',
        'format': 'msdos',
        'mount-order': [1, 0],
        'uuid': UUID[:8],
        'partitions': [
            {
                'name': 'bootfs',
                'partuuid': UUID[:8]+'-01',
                'start': '1MiB',
                'end': '256MiB',
                'format': 'vfat',
                'mount-point': '/boot',
                'mount-options': 'noatime',
                'flags': {
                    'lba': 'on'
                }
            },
            {
                'name': 'rootfs',
                'partuuid': UUID[:8]+'-02',
                'start': '256MiB',
                'end': '100%',
                'format': 'btrfs',
                'mount-point': '/',
                'mount-options': 'noatime,compress=zstd:15,ssd,discard',
                'args': f'--force'
            }
        ]
    }
}

GenPi64OpenRC = GenPi64 | {
    "initsystem": "openrc",
    "initramfs": "none",
    "service-manager": "rcupdate_add",
    "portage": GenPi64['portage'] | {
        "make.conf": GenPi64['portage']['make.conf'] | {
            "USE": GenPi64["portage"]["make.conf"]["USE"] + ["-systemd", "elogind"]
        }
    },
    'image': GenPi64['image'] | {
        'name': 'GenPi64OpenRC.img'
    },
    "services": {
        "cronie": "default",
        "sshd": "default",
        "swclock": "shutdown",
        "elogind": "default",
        "rsyslog": "default",
        "chronyd": "default",
        "rngd": "boot",
        "rpi3-ondemand": "default"
    },
}

GenPi64OpenRCDesktop = GenPi64OpenRC | {
    "profile": "genpi64:default/linux/arm64/17.0/genpi64/desktop",
    'image': GenPi64OpenRC['image'] | {
        'name': 'GenPi64OpenRCDesktop.img'
    },
    'etc': GenPi64OpenRC['etc'] | {
        'env.d/': {
            '90xsession': {'XSESSION':"Xfce4"}
        }
    }
}

GenPi32OpenRC = GenPi64OpenRC | {
    "stage3": "stage3-armv6j_hardfp.tar.xz",
    "stage3url": "http://distfiles.gentoo.org/releases/arm/autobuilds/latest-stage3-armv6j_hardfp.txt",
    "stage3mirror": "http://distfiles.gentoo.org/releases/arm/autobuilds/",
    "portage": GenPi64OpenRC['portage'] | {
        "make.conf": GenPi64OpenRC['portage']['make.conf'] | {
            "CFLAGS": "-O2 -pipe -march=armv6j -mfpu=vfp -mfloat-abi=hard -fomit-frame-pointer -fno-stack-protector",
            "CHOST": "armv6j-unknown-linux-gnueabihf"
        }
    },
    'image': GenPi64OpenRC['image'] | {
        'name': 'GenPi32OpenRC.img'
    },
    "profile": "default/linux/arm/17.0"
}

GenPi64Systemd = GenPi64 | {
    "kernel": GenPi64["kernel"] + ["sys-kernel/dracut"],
    "initramfs": "dracut",
    "initsystem": "systemd",
    "service-manager": "systemctl_enable",
    "stage3": os.environ.get("STAGE3", "stage3-arm64-systemd.tar.xz"),
    "stage3url": "http://distfiles.gentoo.org/releases/arm64/autobuilds/latest-stage3-arm64-systemd.txt",
    "stage3mirror": "http://distfiles.gentoo.org/releases/arm64/autobuilds/",
    "profile": "genpi64:default/linux/arm64/17.0/genpi64/systemd",
    "portage": GenPi64["portage"] | {
        "make.conf": GenPi64["portage"]["make.conf"] | {
            "USE": GenPi64["portage"]["make.conf"]["USE"] + ["systemd", "-elogind"],
        }
    },
    "etc": GenPi64["etc"] | {
        "systemd/": {
            "network/": {
                i: "systemd/network/" + i for i in os.listdir(os.path.join(os.environ.get('CONFIG_DIR'), 'systemd/network'))
            }
        }
    },
    "services": {
        "tmp.mount": "mask",
        "sshd.socket": "enable",
        "gpm.service": "enable",
        "rngd.service": "enable",
        "zram_tmp.service": "enable",
        "zram_swap.service": "enable",
        "zram_var_tmp.service": "enable",
        "systemd-networkd.service": "enable",
        "systemd-resolved.service": "enable",
        "systemd-timesyncd.service": "enable"
    },
    'image': GenPi64['image'] | {
        'name': 'GenPi64Systemd.img'
    }
}

GenPi64SystemdDesktop = GenPi64Systemd | {
    "profile": "genpi64:default/linux/arm64/17.0/genpi64/desktop/systemd",
    'image': GenPi64Systemd['image'] | {
        'name': 'GenPi64SystemdDesktop.img'
    }
}

GentooAMD64 = Base | {
    "initsystem": "openrc",
    "initramfs": "none",
    "service-manager": "rcupdate_add",
    "stage3": "stage3-amd64.tar.xz",
    "stage3url": "http://distfiles.gentoo.org/releases/amd64/autobuilds/latest-stage3-amd64.txt",
    "stage3mirror": "http://distfiles.gentoo.org/releases/amd64/autobuilds/",
    "profile": "default/linux/amd64/17.1",
    'sets': ['standard', 'amd64'],
    'portage': Base['portage'] | {
        "make.conf": Base['portage']['make.conf'] | {
            'CHOST': 'x86_64-unknown-linux-gnu',
            "USE": 'bindist -systemd openssl'.split(),
            'GRUB_PLATFORMS': "pc",
        },
        "package.license/": {
          "linux-firmware": [ "sys-kernel/linux-firmware linux-fw-redistributable no-source-code" ],
        },
        "env/": {},
        "package.env/": {},
        "package.use/": {},
    },
    "overlays": [
        {
            'name': 'gentoo',
            'location': '/var/db/repos/gentoo',
            'sync-type': 'git',
            'clone-depth': '1',
            'sync-depth': '1',
            'sync-uri': 'https://github.com/gentoo-mirror/gentoo',
            'auto-sync': 'yes',
            'sync-git-verify-commit-signature': 'true',
            "#commit-hash": "HEAD",
            "#clone-date": "2021-03-31",
        },
        {
            'name': 'genpi64',
            'location': '/var/db/repos/genpi64',
            'sync-type': 'git',
            'sync-uri': 'https://github.com/GenPi64/genpi64-overlay.git',
            'priority': '100',
            'auto-sync': 'yes',
            'clone-depth': '1',
            'sync-depth': '1',
            "#commit-hash": "HEAD",
            "#clone-date": "2021-03-31",
        },
        {
            'name': 'genpi-tools',
            'location': '/var/db/repos/genpi-tools',
            'sync-type': 'git',
            'sync-uri': 'https://github.com/GenPi64/genpi-tools.git',
            'priority': '50',
            'auto-sync': 'yes',
            'clone-depth': '1',
            'sync-depth': '1',
            "#commit-hash": "HEAD",
            "#clone-date": "2021-03-31",
        }
    ],
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
        "dhcpcd": "default",
        "elogind": "default",
        "rsyslog": "default",
        "chronyd": "default",
        "qemu-guest-agent": "default"
    },
    'image': GenPi64['image'] | {
        'name': 'GentooAMD64Server.img',
        'format': 'msdos',
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
