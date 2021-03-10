#!/usr/bin/python3

import os
import sys
import uuid

chroot_cmd = os.environ.get('CHROOT_CMD', 'pychroot')

if chroot_cmd == 'pychroot':
    os.execvpe(chroot_cmd, ['pychroot', '-B', '%s:/var/cache/binpkgs' %os.path.join(os.environ['PROJECT_DIR'], 'packages'), os.environ['CHROOT_DIR'], *sys.argv[1:]], os.environ)

elif chroot_cmd == 'systemd-nspawn':
    os.execvpe('systemd-nspawn', [f'--machine={uuid.uuid4()}', f'--directory="{os.environ["CHROOT_DIR"]}"', '--bind', ('%s:/var/cache/binpkgs' % os.path.join(os.environ['PROJECT_DIR'], 'packages')), *sys.argv[1:]], os.environ)
               
    

    
else:
    raise RuntimeError("Unknown chroot command: "+chroot_cmd)
