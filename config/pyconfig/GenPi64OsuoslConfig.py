import os
from .BaseConfig import Base, UUID

GenPi64Osuosl = Base | {
    "kernel": [
        "sys-kernel/dracut",
        "sys-kernel/gentoo-kernel",
        "sys-kernel/installkernel-systemd"
    ],
    "initramfs": "dracut",
    "initsystem": "systemd",
    "service-manager": "systemctl_enable",
    "portage": Base["portage"] | {
        "make.conf": Base["portage"]["make.conf"] | {
            "CFLAGS": "${CFLAGS} -ftree-vectorize -O2 -pipe",
            "CXXFLAGS": "${CFLAGS}",
            "FCFLAGS": "${CFLAGS}",
            "FFLAGS": "${CFLAGS}",
            "CHOST": "aarch64-unknown-linux-gnu",
            "MAKEOPTS": "-j4 -l4",
            "FEATURES": Base["portage"]["make.conf"][
                            "FEATURES"] + "-userpriv -usersandbox -network-sandbox -pid-sandbox".split(),
            "USE": Base["portage"]["make.conf"]["USE"] + ["gnuefi boot kernel-install"],
        }
    },
    "etc": Base["etc"] | {
        "hostname": "hostname",
        "systemd/": {
            "network/": {
                i: "systemd/network/" + i for i in os.listdir(os.path.join(os.environ.get('CONFIG_DIR'), 'systemd/network'))
            }
        },
        "portage/": {
            "patches/": {
                "sys-apps/": {
                    "systemd/": {
                        i: "patches/sys-apps/systemd/" + i for i in os.listdir(os.path.join(os.environ.get('CONFIG_DIR'), 'patches/sys-apps/systemd'))
                    }
                }
            }
        },
        "repart.d/": {
            i: "repart.d/" + i for i in os.listdir(os.path.join(os.environ.get('CONFIG_DIR'), 'repart.d'))
        },
        "kernel/": {
            i: "kernel/" + i for i in os.listdir(os.path.join(os.environ.get('CONFIG_DIR'), 'kernel'))
        },
        "dracut.conf.d/": {
            i: "dracut.conf.d/" + i for i in os.listdir(os.path.join(os.environ.get('CONFIG_DIR'), 'dracut.conf.d'))
        }
    },
    "stage3": os.environ.get("STAGE3", "stage3-arm64.tar.xz"),
    "stage3url": "https://mirror.init7.net/gentoo/releases/arm64/autobuilds/latest-stage3-arm64-systemd-mergedusr.txt",
    "stage3mirror": "https://mirror.init7.net/gentoo/releases/arm64/autobuilds/",
    "profile": "gentoo:default/linux/arm64/17.0/systemd/merged-usr",
    "packages": [
        "app-portage/gentoolkit",
        "app-emulation/cloud-init"
    ],
    "services": {
        "gpm.service": "enable",
        "sshd.service": "enable",
        "rngd.service": "enable",
        "cloud-init.service": "enable",
        "console-getty.service": "enable",
        "systemd-oomd.service": "enable",
        "systemd-pstore.service": "enable",
        "systemd-networkd.socket": "disable",
        "systemd-networkd.service": "enable",
        "systemd-resolved.service": "enable",
        "systemd-timesyncd.service": "enable",
        "systemd-network-generator.service": "enable",
        "systemd-networkd-wait-online.service": "disable"
    },
    'image': {
        'name': 'GenPi64Osuosl.img',
        'size': '8G',
        'format': 'gpt',
        'mount-order': [2, 1, 0],
        'uuid': UUID[:8],
        'partitions': [
            {
              'name': 'EFI System Partition',
              'partuuid': UUID[:8]+'-01',
              'typeuuid': 'c12a7328-f81f-11d2-ba4b-00a0c93ec93b',
              'start': '1MiB',
              'end': '256MiB',
              'filesystem': 'vfat',
              'mount-point': '/efi',
              'mount-options': 'noatime',
              'fstab-dump': 0,
              'fstab-fsck-pass': 1
            },
            {
              'name': 'Extended Boot Loader Partition',
              'partuuid': UUID[:8]+'-02',
              'typeuuid': 'c12a7328-f81f-11d2-ba4b-00a0c93ec93b',
              'start': '256MiB',
              'end': '512MiB',
              'filesystem': 'vfat',
              'mount-point': '/boot',
              'mount-options': 'noatime',
              'fstab-dump': 0,
              'fstab-fsck-pass': 1
            },
            {
              'name': 'Root Partition (64-bit ARM/AArch64)',
              'partuuid': UUID[:8]+'-03',
              'typeuuid': 'b921b045-1df0-41c3-af44-4c6f280d3fae',
              'start': '512MiB',
              'end': '100%',
              'filesystem': 'btrfs',
              'mount-point': '/',
              'mount-options': 'noatime,x-systemd.growfs',
              'args': '--force',
              'fstab-dump': 0,
              'fstab-fsck-pass': 0
            }
        ]
    }
}
