<<<<<<< HEAD
#!/bin/bash

=======
export BASEDIR=$(pwd)
>>>>>>> 3f0ec8ad7cc7cd33652477e5ad20fdc1d358e9e8

echo $PROJECT
if [[ -z "$PROJECT" ]]; then
	export PROJECT="gentoo-arm"
fi

if [[ -z "$PROJECT_DIR" ]]; then
	export PROJECT_DIR="${BASEDIR}/build/${PROJECT}"
fi


echo $PROJECT
#This list of variables must also be included in the copyenv directive of parsers/include
#export PROJECT_DIR="${BASEDIR}/build/${PROJECT}"
export CONFIG_DIR="${BASEDIR}/config"
export CHROOT_DIR="${PROJECT_DIR}/chroot"
export PARSERS="${BASEDIR}/parsers"
export BINARY_ASSETS="${BASEDIR}/build-binary-assets"
export SCRIPTS="${BASEDIR}/scripts"
export CALLBACKS="${BASEDIR}/callbacks"
