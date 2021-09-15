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

OuterChroot = {
    'portage': {
        "make.conf": dict(
            CFLAGS="-march=native -O2 -pipe",
            CXXFLAGS="${CFLAGS}",
            FCFLAGS="${CFLAGS}",
            FFLAGS="${CFLAGS}",
            USE=["bindist"],
            FEATURES="parallel-fetch parallel-install ".split(),
            MAKEOPTS=f"-j{len(os.sched_getaffinity(0))} -l{len(os.sched_getaffinity(0))}",
            VIDEO_CARDS="",
            LLVM_TARGETS="AMDGPU BPF NVPTX (X86) AArch64 ARM",
            QEMU_USER_TARGETS="aarch64 arm"
        ),
        "package.accept_keywords/": {
            "pychroot": "package.accept_keywords"
        },
        "patches/": {
            "app-editors/": "patches/app-editors",
            "sys-apps/": "patches/sys-apps",
            "dev-lang/": "patches/dev-lang"
        },
    },
    "etc": {
        "locale.gen": "locale.gen",
        "profile": "profile"
    },
    "jobs": len(os.sched_getaffinity(0)),
    "load-average": len(os.sched_getaffinity(0)),
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
            "#commit-hash": "f55aa0ddaa3f35701531dfd72d557799be18e2a0",
            "#clone-date": "2021-06-10",

        }
    ],
    "packages": [
        "dev-python/pychroot ",
        "sys-devel/gcc ",
        "sys-devel/clang "
        "acct-user/distcc ",
        "app-emulation/qemu "
    ],
    "stage3": os.environ.get("STAGE3", "stage3-amd64.tar.xz"),
    "stage3url": "http://distfiles.gentoo.org/releases/amd64/autobuilds/latest-stage3-amd64.txt",
    "stage3mirror": "http://distfiles.gentoo.org/releases/amd64/autobuilds/",
    "profile": "default/linux/amd64/17.1",
    "target": "GenPi64OpenRCDesktop",
    "target-branch": "alpha9"
    
}
