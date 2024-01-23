from .GenAMD64UefiSystemdConfig import GenAMD64UefiSystemd

GenAMD64UefiSystemdPlasmaDesktop = GenAMD64UefiSystemd | {
    "profile": "gentoo:default/linux/amd64/17.1/desktop/plasma/systemd/merged-usr",
    'image': GenAMD64UefiSystemd['image'] | {
        'name': 'GenAMD64UefiSystemdPlasmaDesktop.img'
    }
}
