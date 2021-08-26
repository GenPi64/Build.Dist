#!/usr/bin/env python3

import os
import sys
import uuid

if not os.path.exists(os.path.join(os.environ['PROJECT_DIR'], 'packages')):
    os.mkdir(os.path.join(os.environ['PROJECT_DIR'], 'packages'))

# Retain old behavior
if 'CHROOT_CMD' in os.environ:
    chroot_cmd = os.environ.get('CHROOT_CMD')
    if chroot_cmd == 'pychroot':
        os.execvpe('pychroot',
                   ['pychroot', '-B', '%s:/var/cache/binpkgs' % os.path.join(os.environ['PROJECT_DIR'], 'packages'),
                    os.environ['CHROOT_DIR'], *sys.argv[1:]], os.environ)
    elif chroot_cmd == 'systemd-nspawn':
        os.execvpe('systemd-nspawn',
                   ['systemd-nspawn', f'--machine={uuid.uuid4()}', f'--directory={os.environ["CHROOT_DIR"]}', '--bind',
                    ('%s:/var/cache/binpkgs' % os.path.join(os.environ['PROJECT_DIR'], 'packages')), *sys.argv[1:]],
                   os.environ)

# Add new behavior
elif os.path.exists('/sbin/openrc-run'):
    os.execvpe('pychroot',
               ['pychroot', '-B', '%s:/var/cache/binpkgs' % os.path.join(os.environ['PROJECT_DIR'], 'packages'),
                os.environ['CHROOT_DIR'], *sys.argv[1:]], os.environ)
elif 'systemd' in os.readlink('/proc/1/exe'):
    os.execvpe('systemd-nspawn',
               ['systemd-nspawn', f'--machine={uuid.uuid4()}', f'--directory={os.environ["CHROOT_DIR"]}', '--bind',
                ('%s:/var/cache/binpkgs' % os.path.join(os.environ['PROJECT_DIR'], 'packages')), *sys.argv[1:]],
               os.environ)
else:
    raise RuntimeError("Unknown error occured, probably because I couldn't figure out the init system automatically"
                       " or CHROOT_CMD env variable was not manually set.")
