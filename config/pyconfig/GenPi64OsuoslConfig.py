import os
from .GenPi64UefiSystemdConfig import GenPi64UefiSystemd

GenPi64Osuosl = GenPi64UefiSystemd | {
    "portage": GenPi64UefiSystemd["portage"] | {
        "make.conf": GenPi64UefiSystemd["portage"]["make.conf"] | {
            "CHOST": "aarch64-unknown-linux-gnu"
        }
    },
    "stage3": os.environ.get("STAGE3", "stage3-arm64.tar.xz"),
    "stage3url": "https://mirror.init7.net/gentoo/releases/arm64/autobuilds/latest-stage3-arm64-systemd-mergedusr.txt",
    "stage3mirror": "https://mirror.init7.net/gentoo/releases/arm64/autobuilds/",
    "profile": "gentoo:default/linux/arm64/17.0/systemd/merged-usr",
    'image': GenPi64UefiSystemd["image"] | {
        'name': 'GenPi64Osuosl.img'
    }
}

GenPi64Osuosl["image"]["partitions"][2]["partlabel"] = 'Root Partition 64-bit ARM/AArch64'
GenPi64Osuosl["image"]["partitions"][2]["typeuuid"] = 'B921B045-1DF0-41C3-AF44-4C6F280D3FAE'
