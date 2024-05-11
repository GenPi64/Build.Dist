from .GenAMD64UefiSystemdConfig import GenAMD64UefiSystemd

GenAMD64UefiSystemdPlasmaDesktop = GenAMD64UefiSystemd | {
    "profile": "gentoo:default/linux/amd64/23.0/desktop/plasma/systemd",
    'image': GenAMD64UefiSystemd['image'] | {
        'name': 'GenAMD64UefiSystemdPlasmaDesktop.img'
    }
}
