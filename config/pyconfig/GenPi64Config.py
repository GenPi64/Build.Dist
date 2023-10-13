import os
from .BaseConfig import Base, UUID


GenPi64 = Base | {
    "cmdline": 'console=serial0,115200 console=tty1 dwc_otg.lpm_enable=0 root=PARTUUID=%(PARTUUID)s rootfstype=%(fstype)s fsck.repair=no usbhid.mousepoll=0 rootdelay=10 init=/sbin/init',
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
            'sync-git-clone-extra-opts': '--single-branch --branch master',
            "#commit-hash": "HEAD",
            "#clone-date": "2021-08-24"
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
            "#clone-date": "2021-01-01"
        }
    ],
    "portage": Base["portage"] | {
        "make.conf": Base["portage"]["make.conf"] | {
            "CFLAGS": "${CFLAGS} -march=armv8-a+crc -mtune=cortex-a72 -ftree-vectorize -O2 -pipe",
            "CXXFLAGS": "${CFLAGS}",
            "FCFLAGS": "${CFLAGS}",
            "FFLAGS": "${CFLAGS}",
            "CHOST": "aarch64-unknown-linux-gnu",
            "MAKEOPTS": "-j4 -l4",
            "FEATURES": Base["portage"]["make.conf"][
                            "FEATURES"] + "-userpriv -usersandbox -network-sandbox -pid-sandbox".split(),
            "USE": Base["portage"]["make.conf"]["USE"] + ["-checkboot"],
            "VIDEO_CARDS": ["vc4"] + ["v3d"] + ["fbdev"]
        },
        "package.mask": "package.mask",
        "package.accept_keywords": "package.accept_keywords"
    },
    "etc": Base["etc"] | {
        "dhcpcd.conf": "dhcpcd.conf",
        "hostname": "hostname",
        "portage/": {
            "binrepos.conf/": {
                "genpi64binhost.conf" : "genpi64binhost.conf"
            }
        }
    },
    "stage3": os.environ.get("STAGE3", "stage3-arm64.tar.xz"),
    "stage3url": "https://mirror.init7.net/gentoo/releases/arm64/autobuilds/latest-stage3-arm64-openrc.txt",
    "stage3mirror": "https://mirror.init7.net/gentoo/releases/arm64/autobuilds/",
    "profile": "genpi64:default/linux/arm64/17.0/genpi64",
    'users': [
        Base['users'][0] | dict(
            password="Raspberrypi64!",
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
              'typeuuid': 'c12a7328-f81f-11d2-ba4b-00a0c93ec93b',
              'mbrtypeid': 'c',
              'start': '1MiB',
              'end': '256MiB',
              'filesystem': 'vfat',
              'mount-point': '/boot',
              'mount-options': 'noatime',
              'flags': {
                'boot': 'on'
              },
              'fstab-dump': 0,
              'fstab-fsck-pass': 1
            },
            {
              'name': 'rootfs',
              'partuuid': UUID[:8]+'-02',
              'typeuuid': 'b921b045-1df0-41c3-af44-4c6f280d3fae',
              'mbrtypeid': '83',
              'start': '256MiB',
              'end': '100%',
              'filesystem': 'btrfs',
              'mount-point': '/',
              'mount-options': 'noatime,compress=zstd:15,ssd,discard,x-systemd.growfs',
              'args': '--force',
              'fstab-dump': 0,
              'fstab-fsck-pass': 0
            }
        ]
    }
}
