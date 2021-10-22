from GenPi64OpenRCConfig import GenPi64OpenRC

GenPi32OpenRC = GenPi64OpenRC | {
    "stage3": "stage3-armv6j_hardfp.tar.xz",
    "stage3url": "http://bouncer.gentoo.org/fetch/root/all/releases/arm/autobuilds/latest-stage3-armv6j_hardfp.txt",
    "stage3mirror": "http://bouncer.gentoo.org/fetch/root/all/releases/arm/autobuilds/",
    "portage": GenPi64OpenRC['portage'] | {
        "make.conf": GenPi64OpenRC['portage']['make.conf'] | {
            "CFLAGS": "-O2 -pipe -march=armv6j -mfpu=vfp -mfloat-abi=hard -fomit-frame-pointer -fno-stack-protector",
            "CHOST": "armv6j-unknown-linux-gnueabihf"
        }
    },
    'image': GenPi64OpenRC['image'] | {
        'name': 'GenPi32OpenRC.img'
    },
    "profile": "default/linux/arm/17.0"
}