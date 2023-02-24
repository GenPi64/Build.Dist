import os
import uuid
from .GentooAMD64Config import GentooAMD64, UUID

UUIDs = [UUID]

for idx in range(1, 4):
    if os.path.exists(p := os.path.join(os.environ['PROJECT_DIR'], f'uuid-p{idx}')):
        with open(p) as f:
            UUIDs.append(f.read())
    else:
        UUIDs.append(str(uuid.uuid4()))
        with open(p, 'w') as f:
            f.write(UUIDs[-1])


GentooAMD64Systemd = GentooAMD64 | {
    "initsystem": "systemd",
    "initramfs": "none",
    "service-manager": "systemctl_enable",
    "stage3": "stage3-amd64-systemd-mergedusr.tar.xz",
    "stage3url": "http://bouncer.gentoo.org/fetch/root/all/releases/amd64/autobuilds/latest-stage3-amd64-systemd-mergedusr.txt",
    "stage3mirror": "http://bouncer.gentoo.org/fetch/root/all/releases/amd64/autobuilds",
    "profile": "default/linux/amd64/17.1/systemd/merged-usr",
    'portage': GentooAMD64['portage'] | {
        "make.conf": GentooAMD64['portage']['make.conf'] | {
            'CFLAGS': '${CFLAGS} -march=x86-64 -mtune=generic -pipe',
            'CHOST': 'x86_64-pc-linux-gnu',
            "USE": 'bindist systemd openssl'.split(),
            'GRUB_PLATFORMS': "pc",
        },
        "env/": {},
        "package.env/": {},
        "package.use/": {},
    },
    "etc": GentooAMD64["etc"] | {
        "systemd/": {
            "network/": {
                i: "systemd/network/" + i for i in os.listdir(os.path.join(os.environ.get('CONFIG_DIR'), 'systemd/network'))
            }
        },
        "repart.d/": {
            i: "repart.d/" + i for i in os.listdir(os.path.join(os.environ.get('CONFIG_DIR'), 'repart.d'))
        }
    },
    "services": {
        "tmp.mount": "mask",
        "gpm.service": "enable",
        "sshd.service": "enable",
        "rngd.service": "enable",
        "zram_tmp.service": "enable",
        "zram_swap.service": "enable",
        "zram_var_tmp.service": "enable",
        "systemd-oomd.service": "enable",
        "systemd-pstore.service": "enable",
        "systemd-networkd.service": "enable",
        "systemd-resolved.service": "enable",
        "systemd-timesyncd.service": "enable",
        "systemd-network-generator.service": "enable",
        "systemd-networkd-wait-online.service": "disable"
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
    'image': GentooAMD64['image'] | {
        'name': 'GentooAMD64SystemdSrv.img',
        'size': '16G',
        'format': 'gpt',
        'mount-order': [2, 1, 0],
        'uuid': UUID
    }
}
