# Build.Dist
Build scripts for building GenPi64 images.

## Requirements
Linux system (gcc, chroot, et cetera)
Python3.9
git
dev-python/python-lockfile
dev-python/iniparse
qemu with xattrs enabled.
### Filesystem creation tools
btrfs-progs (or change the filesystem type and mount options in `config/config.py`)
sgdisk (for gpt based disk images)
sfdisk (for mbr based disk images)

### If running from not aarch64
qemu user static for aarch64 and arm

### USE flags when running on Gentoo
- qemu needs to be emerged with USE="static-user".

### Extra requirements if not running on gentoo
wget



## Usage

You need to download the stage 3 tarball you want to use, and put it in `build-binary-assets/stage3`.
Edit `config/config.py` and update the path to the stage3 version you're using.

Pick a target by running
`export PROJECT=<projectname>` 
default is `GenPi64OpenRC`.  

If you want to set where the build should happen, run
`export PROJECT_DIR=</path/to/build/location>`
default is `$PWD/build/$PROJECT`.

Then run `sh build.sh`.  Wait (a *long* time).  At the end, you should have your output in `$PROJECT_DIR`.  
Packages are in `$PROJECT_DIR/packages`, the image file is in `$PROJECT_DIR/`.  There's also a stage4 generated, 
in the same location.

There's a convenience script `source set-env.sh` that will export the useful variables for you, mostly used by the project maintainers to run a build of our own.

If you are building an arm target via qemu, you probably want a distcc server running with crossdev gcc as it takes DAYS to build.

## Config

You can configure the project via `config/pyconfig/*.py`, each PROJECT has its own config file.  
The default is `GenPi64OpenRC`.  You can override the default by setting `PROJECT` in the environment.
The steps to execute are governed by the `.json` files in the project root.

## Troubleshooting

Compiling python often hangs running `compileall.py`.  It's safe to kill the hung tasks.  

If `. env.sh` you can manually run a parser and better assess its output.  You can also `./chroot.sh` and manually tweak things inside the prefix.

### QEMU

If you're getting either of these errors, you probably need to install qemu user static and configure it for the target arch.
```
exec format
bad interpreter
```
