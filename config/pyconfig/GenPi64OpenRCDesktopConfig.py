from GenPi64OpenRCConfig import GenPi64OpenRC

GenPi64OpenRCDesktop = GenPi64OpenRC | {
    "profile": "genpi64:default/linux/arm64/17.0/genpi64/desktop",
    'image': GenPi64OpenRC['image'] | {
        'name': 'GenPi64OpenRCDesktop.img'
    },
    'etc': GenPi64OpenRC['etc'] | {
        'env.d/': {
            '90xsession': {'XSESSION':"Xfce4"}
        }
    }
}
