from GentooAMD64Config import GentooAMD64

GentooAMD64OpenRCDesktop = GentooAMD64 | {
    'profile': "default/linux/amd64/17.1/desktop/plasma",
    'portage': GentooAMD64['portage'] | {
        "make.conf": GentooAMD64['portage']['make.conf'] | {
            "USE": 'elogind dbus openssl pulseaudio bluetooth ipv6 -systemd -cups pcsc-lite samba'.split(),
            'GRUB_PLATFORMS': 'efi-64',
            'VIDEO_CARDS': 'intel i965 iris',
        },
    },
    'image': GentooAMD64['image'] | {
        'name': 'GentooAMD64Desktop.img',
        'size': '16G'
    }
}
