import os
from .GenAMD64UefiSystemdConfig import GenAMD64UefiSystemd

GenPi64Osuosl = GenAMD64UefiSystemd | {
    "portage": GenAMD64UefiSystemd["portage"] | {
        "make.conf": GenAMD64UefiSystemd["portage"]["make.conf"] | {
            "CHOST": "aarch64-unknown-linux-gnu"
        }
    },
    "etc": GenAMD64UefiSystemd["etc"] | {
        "kernel/": GenAMD64UefiSystemd["etc"]["kernel/"] | {
            "config.d/": {
                "EFI_ZBOOT.config" : "osuosl/etc/kernel/config.d/EFI_ZBOOT.config"
            }
        },
        "portage/": GenAMD64UefiSystemd["etc"]["portage/"]
    },
    "stage3": os.environ.get("STAGE3", "stage3-arm64.tar.xz"),
    "stage3url": "https://mirror.init7.net/gentoo/releases/arm64/autobuilds/latest-stage3-arm64-systemd.txt",
    "stage3mirror": "https://mirror.init7.net/gentoo/releases/arm64/autobuilds/",
    "profile": "gentoo:default/linux/arm64/23.0/systemd",
    'image': GenAMD64UefiSystemd["image"] | {
        'name': 'GenPi64Osuosl.img'
    }
}

GenPi64Osuosl["image"]["partitions"][2]["partlabel"] = 'Root Partition 64-bit ARM/AArch64'
GenPi64Osuosl["image"]["partitions"][2]["typeuuid"] = 'B921B045-1DF0-41C3-AF44-4C6F280D3FAE'
