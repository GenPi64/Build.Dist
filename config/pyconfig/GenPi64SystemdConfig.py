import os
from .GenPi64Config import GenPi64

GenPi64Systemd = GenPi64 | {
    "kernel": GenPi64["kernel"] + ["sys-kernel/dracut"],
    "initramfs": "dracut",
    "initsystem": "systemd",
    "service-manager": "systemctl_enable",
    "stage3": os.environ.get("STAGE3", "stage3-arm64-systemd.tar.xz"),
    "stage3url": "http://bouncer.gentoo.org/fetch/root/all//releases/arm64/autobuilds/latest-stage3-arm64-systemd.txt",
    "stage3mirror": "http://bouncer.gentoo.org/fetch/root/all/releases/arm64/autobuilds/",
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
        },
        "repart.d/": {
            i: "repart.d/" + i for i in os.listdir(os.path.join(os.environ.get('CONFIG_DIR'), 'repart.d'))
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
