import os
import uuid

if os.path.exists(p := os.path.join(os.environ['PROJECT_DIR'], 'uuid')):
    with open(p) as f:
        UUID = f.read()
else:
    UUID = str(uuid.uuid4())
    with open(p, 'w') as f:
        f.write(UUID)


def readlines(p):
    with open(p) as f:
        return (i.split('#', 1)[0].strip() for i in f.read().split('\n'))


Base = {
    'portage': {
        "make.conf": dict(
            CFLAGS="${CFLAGS} -march=native -O2 -pipe",
            CXXFLAGS="${CFLAGS}",
            FCFLAGS="${CFLAGS}",
            FFLAGS="${CFLAGS}",
            USE=["bindist"],
            FEATURES="buildpkg binpkg-multi-instance clean-logs compress-build-logs parallel-fetch parallel-install userfetch usersync ccache ".split(),
            MAKEOPTS=f"-j{len(os.sched_getaffinity(0))} -l{len(os.sched_getaffinity(0))}",
            VIDEO_CARDS="",
            INPUT_DEVICES="libinput",
            BINPKG_FORMAT="gpkg",
            BINPKG_COMPRESS="zstd",
            BINPKG_COMPRESS_FLAGS="-15",
            PORTAGE_COMPRESS="zstd",
            PORTAGE_COMPRESS_FLAGS="-15",
            PORTAGE_NICENESS="20",
            EMERGE_DEFAULT_OPTS="--jobs --newrepo --newuse --changed-use --changed-deps --changed-slot --deep --tree --unordered-display --nospinner --backtrack=3000 --complete-graph --with-bdeps=y --rebuild-if-new-rev --rebuild-if-new-ver --rebuild-if-unbuilt --rebuilt-binaries --binpkg-respect-use=y --binpkg-changed-deps=y --usepkg=y --buildpkg-exclude='virtual/*' --buildpkg-exclude='sys-kernel/*-sources' --buildpkg-exclude='*/*-bin' --buildpkg-exclude='acct-user/*' --buildpkg-exclude='acct-group/*' --buildpkg-exclude='dev-perl/*' --usepkg-exclude='virtual/*' --usepkg-exclude='sys-kernel/*-sources' --usepkg-exclude='*/*-bin' --usepkg-exclude='acct-user/*' --usepkg-exclude='acct-group/*' --usepkg-exclude='dev-perl/*'"
        ),
        #"patches/": {
        #    {}
        #},
        "savedconfig/": {
            "sys-kernel/": {
                "linux-firmware": "linux-firmware"
            }
        },
        "env/": {
            "enable-distcc": ['FEATURES="${FEATURES} distcc"'],
            "dev-lang/": {"python": "patches/python-env"}
        },
        "package.env/": {
            "distcc": [[pn, " enable-distcc"] for pn in
                       readlines(os.path.join(os.environ.get('CONFIG_DIR'), 'distcc-pkgs')) if pn]
        }
    },
    "etc": {
        "kernel/": {
            "config.d/": {
                i: "kernel-config/" + i for i in os.listdir(os.path.join(os.environ.get('CONFIG_DIR'), 'kernel-config'))
            }
        },
        "locale.gen": "locale.gen",
        "profile": "profile"
    },
    "TERM": os.environ['TERM'],
    "jobs": len(os.sched_getaffinity(0)),
    "load-average": len(os.sched_getaffinity(0)),
    "distcc": [
        os.environ.get("DISTCC_HOSTS", "")
    ],
    "groups": [
        dict(name="cron", gid=16),
    ],
    "users": [
        dict(name="demouser",
             password="password",
             format="SHA512",
             group="users",
             groups="users,wheel,video,audio,adm,disk,lp,cdrom,usb,portage,cron".split(','),
             shell="/bin/bash",
             uid="1000"
             )
    ],
    "locale": "en_US.utf8",
    "overlays": [
        {
            'name': 'gentoo',
            'location': '/var/db/repos/gentoo',
            'sync-type': 'git',
            'clone-depth': '1',
            'sync-depth': '1',
            'sync-uri': 'https://github.com/gentoo-mirror/gentoo',
            'auto-sync': 'yes',
            'sync-git-verify-commit-signature': 'true',
            "#commit-hash": "HEAD",
            "#clone-date": "2023-01-01",
        }
    ],
    'sets': [],
    'packages': []
}
