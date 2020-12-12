# Build.Dist
Build scripts for building GenPi64 images.

## Requirements
Linux system (gcc, chroot, et cetera)
Python3.9
pychroot
git


## Usage

You need to download the stage 3 tarball you want to use, and put it in `build-binary-assets/stage3`.
Edit `config/config.py` and update the path to the stage3 version you're using.

Pick a target by running
`export PROJECT=<projectname>` 
default is `GenPi64`.  

If you want to set where the build should happen, run
`export PROJECT_DIR=</path/to/build/location>`
default is `$PWD/build/$PROJECT`.

Then run `sh build.sh`.  Wait (a *long* time).  At the end, you should have your output in `$PROJECT_DIR`.  
Packages are in `$PROJECT_DIR/packages`, the image file is in `$PROJECT_DIR/`.  There's also a stage4 generated, 
in the same location.

If you are building an arm target via qemu, you probably want a distcc server running with crossdev gcc.  

## Config

You can configure the project via `config/config.py`, the default one is fairly fleshed out, so feel free to poke at it to see how it works.
The steps to execute are governed by the `.json` files in the project root.
