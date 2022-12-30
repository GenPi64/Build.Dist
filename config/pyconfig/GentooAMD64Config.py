import os
import uuid
from .BaseConfig import Base, UUID

UUIDs = [UUID]

for idx in range(1, 4):
    if os.path.exists(p := os.path.join(os.environ['PROJECT_DIR'], f'uuid-p{idx}')):
        with open(p) as f:
            UUIDs.append(f.read())
    else:
        UUIDs.append(str(uuid.uuid4()))
        with open(p, 'w') as f:
            f.write(UUIDs[-1])


GentooAMD64 = Base | {
    "initsystem": "openrc",
    "initramfs": "none",
    "service-manager": "rcupdate_add",
    "stage3": "stage3-amd64.tar.xz",
    "stage3url": "http://bouncer.gentoo.org/fetch/root/all/releases/amd64/autobuilds/latest-stage3-amd64-openrc.txt",
    "stage3mirror": "http://bouncer.gentoo.org/fetch/root/all/releases/amd64/autobuilds",
    "profile": "default/linux/amd64/17.1",
    'portage': Base['portage'] | {
        "make.conf": Base['portage']['make.conf'] | {
            'CFLAGS': '${CFLAGS} -march=x86-64 -mtune=generic -pipe',
            'CHOST': 'x86_64-pc-linux-gnu',
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
    "services": {
        "cronie": "default",
        "sshd": "default",
        "dhcpcd": "default",
        "elogind": "default",
        "rsyslog": "default",
        "chronyd": "default",
        "qemu-guest-agent": "default"
    },
    'image': {
        'name': 'GentooAMD64Srv.img',
        'size': '16G',
        'format': 'gpt',
        'mount-order': [2, 1, 0],
        'uuid': UUID,
        'partitions': [
            {
              'partuuid': UUIDs[1],
              'typeuuid': 'c12a7328-f81f-11d2-ba4b-00a0c93ec93b',
              'start': '1MiB',
              'end': '100MiB',
              'filesystem': 'vfat',
              'mount-point': '/boot/efi',
              'mount-options': 'noatime',
              'flags': {
                'boot': 'on'
              },
              'fstab-dump': 0,
              'fstab-fsck-pass': 2
            },
            {
              'partuuid': UUIDs[2],
              'typeuuid': 'bc13c2ff-59e6-4262-a352-b275fd6f7172',
              'start': '101MiB',
              'end': '500MiB',
              'filesystem': 'vfat',
              'mount-point': '/boot',
              'mount-options': 'noatime',
              'fstab-dump': 0,
              'fstab-fsck-pass': 1
            },
            {
              'partuuid': UUIDs[3],
              'typeuuid': '8484680c-9521-48c6-9c11-b0720656f69e',
              'start': '501MiB',
              'end': '0',
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
