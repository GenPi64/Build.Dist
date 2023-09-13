#!/usr/bin/env python3

import os
import sys
import uuid

if not os.path.exists(os.environ['CCACHE_DIR']):
    os.mkdir(os.environ['CCACHE_DIR'])

if not os.path.exists(os.environ['BINPKGS_DIR']):
    os.mkdir(os.environ['BINPKGS_DIR'])

if not os.path.exists(os.environ['DISTFILES_DIR']):
    os.mkdir(os.environ['DISTFILES_DIR'])

# Retain old behavior
if 'CHROOT_CMD' in os.environ:
    chroot_cmd = os.environ.get('CHROOT_CMD')
    if chroot_cmd == 'pychroot':
        os.execvpe('pychroot',
                   ['pychroot',
                    '-B', f'{os.environ["CCACHE_DIR"]}:/var/tmp/ccache',
                    '-B', f'{os.environ["BINPKGS_DIR"]}:/var/cache/binpkgs',
                    '-B', f'{os.environ["DISTFILES_DIR"]}:/var/cache/distfiles',
                    os.environ['CHROOT_DIR'],
                    *sys.argv[1:]], os.environ)
    elif chroot_cmd == 'systemd-nspawn':
        os.execvpe('systemd-nspawn',
                   ['systemd-nspawn',
                    f'--timezone=off',
                    f'--resolv-conf=bind-host',
                    f'--machine={uuid.uuid4()}',
                    f'--directory={os.environ["CHROOT_DIR"]}',
                    f'--bind={os.environ["CCACHE_DIR"]}:/var/tmp/ccache',
                    f'--bind={os.environ["BINPKGS_DIR"]}:/var/cache/binpkgs',
                    f'--bind={os.environ["DISTFILES_DIR"]}:/var/cache/distfiles',
                    *sys.argv[1:]],
                   os.environ | { "SYSTEMD_SUPPRESS_SYNC" : "1" })

# Add new behavior
elif os.path.exists('/sbin/openrc-run'):
    os.execvpe('pychroot',
               ['pychroot',
                '-B', f'{os.environ["CCACHE_DIR"]}:/var/tmp/ccache',
                '-B', f'{os.environ["BINPKGS_DIR"]}:/var/cache/binpkgs',
                '-B', f'{os.environ["DISTFILES_DIR"]}:/var/cache/distfiles',
                os.environ['CHROOT_DIR'],
                *sys.argv[1:]], os.environ)
elif 'systemd' in os.readlink('/proc/1/exe'):
    os.execvpe('systemd-nspawn',
               ['systemd-nspawn',
                f'--timezone=off',
                f'--resolv-conf=bind-host',
                f'--machine={uuid.uuid4()}',
                f'--directory={os.environ["CHROOT_DIR"]}',
                f'--bind={os.environ["CCACHE_DIR"]}:/var/tmp/ccache',
                f'--bind={os.environ["BINPKGS_DIR"]}:/var/cache/binpkgs',
                f'--bind={os.environ["DISTFILES_DIR"]}:/var/cache/distfiles',
                *sys.argv[1:]],
               os.environ | { "SYSTEMD_SUPPRESS_SYNC" : "1" })
else:
    raise RuntimeError("Unknown error occured, probably because I couldn't figure out the init system automatically"
                       " or CHROOT_CMD env variable was not manually set.")
