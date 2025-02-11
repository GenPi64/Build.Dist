import os
from .GenPi64Config import GenPi64

GenPi64OpenRC = GenPi64 | {
    "initsystem": "openrc",
    "initramfs": "none",
    "service-manager": "rcupdate_add",
    "stage3": os.environ.get("STAGE3", "stage3-arm64-openrc.tar.xz"),
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
