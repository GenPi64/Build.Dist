import os
from .BaseConfig import Base, UUID

import uuid

if os.path.exists(p := os.path.join(os.environ['PROJECT_DIR'], 'partition1Uuid')):
    with open(p) as f:
        partition1Uuid = f.read()
else:
    partition1Uuid = str(uuid.uuid4())
    with open(p, 'w') as f:
        f.write(partition1Uuid)

if os.path.exists(p := os.path.join(os.environ['PROJECT_DIR'], 'partition2Uuid')):
    with open(p) as f:
        partition2Uuid = f.read()
else:
    partition2Uuid = str(uuid.uuid4())
    with open(p, 'w') as f:
        f.write(partition2Uuid)

if os.path.exists(p := os.path.join(os.environ['PROJECT_DIR'], 'partition3Uuid')):
    with open(p) as f:
        partition3Uuid = f.read()
else:
    partition3Uuid = str(uuid.uuid4())
    with open(p, 'w') as f:
        f.write(partition3Uuid)


def readlines(p):
    with open(p) as f:
        return (i.split('#', 1)[0].strip() for i in f.read().split('\n'))


GenAMD64UefiSystemd = Base | {
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
            "CHOST": "x86_64-pc-linux-gnu",
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
    "stage3": os.environ.get("STAGE3", "stage3-amd64.tar.xz"),
    "stage3url": "https://mirror.init7.net/gentoo/releases/amd64/autobuilds/latest-stage3-amd64-desktop-systemd-mergedusr.txt",
    "stage3mirror": "https://mirror.init7.net/gentoo/releases/amd64/autobuilds/",
    "profile": "gentoo:default/linux/amd64/17.1/systemd/merged-usr",
    "packages": [
        "dev-vcs/git",
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
        'name': 'GenAMD64UefiSystemd.img',
        'size': '8G',
        'format': 'gpt',
        'mount-order': [2, 1, 0],
        'uuid': UUID,
        'partitions': [
            {
                'partlabel': 'EFI System Partition',
                'fslabel': 'EFI',
                'partuuid': partition1Uuid,
                'typeuuid': 'C12A7328-F81F-11D2-BA4B-00A0C93EC93B',
                'start': '0',
                'end': '+256MiB',
                'filesystem': 'vfat',
                'mount-point': '/efi',
                'mount-options': 'noatime',
                'fstab-dump': 0,
                'fstab-fsck-pass': 1,
                'flags': {
                    'boot': 'on'
                }
            },
            {
                'partlabel': 'Extended Boot Loader Partition',
                'fslabel': 'XBOOTLDR',
                'partuuid': partition2Uuid,
                'typeuuid': 'BC13C2FF-59E6-4262-A352-B275FD6F7172',
                'start': '0',
                'end': '+256MiB',
                'filesystem': 'vfat',
                'mount-point': '/boot',
                'mount-options': 'noatime',
                'fstab-dump': 0,
                'fstab-fsck-pass': 1
            },
            {
                'partlabel': 'Root Partition (64-bit AMD64/x86_64)',
                'fslabel': 'ROOT',
                'partuuid': partition3Uuid,
                'typeuuid': '4F68BCE3-E8CD-4DB1-96E7-FBCAF984B709',
                'start': '0',
                'end': '0',
                'filesystem': 'btrfs',
                'mount-point': '/',
                'mount-options': 'noatime,x-systemd.growfs',
                'args': '--force',
                'fstab-dump': 0,
                'fstab-fsck-pass': 0,
                'flags': {
                    'grow-file-system': 'on'
                }
            }
        ]
    }
}
