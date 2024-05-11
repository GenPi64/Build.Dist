from .GenPi64SystemdConfig import GenPi64Systemd

GenPi64SystemdDesktop = GenPi64Systemd | {
    "profile": "genpi64:default/linux/arm64/23.0/genpi64/desktop/systemd",
    'image': GenPi64Systemd['image'] | {
        'name': 'GenPi64SystemdDesktop.img'
    }
}
