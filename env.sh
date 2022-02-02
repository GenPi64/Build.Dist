#!/bin/bash
export BASEDIR=${PWD}


if [[ -z "$PROJECT" ]]; then
	export PROJECT="GenPi64OpenRC"
fi

if [[ -z "$PROJECT_DIR" ]]; then
	export PROJECT_DIR="${BASEDIR}/build/${PROJECT}"
fi

if [[ -z "$BINPKGS_DIR" ]] ; then
        export BINPKGS_DIR=${PROJECT_DIR}/packages
fi

if [[ -z "$DISTFILES_DIR" ]] ; then
        export DISTFILES_DIR=${PROJECT_DIR}/distfiles
fi

if [[ -z "$BINARY_ASSETS" ]]; then
	export BINARY_ASSETS="${PROJECT_DIR}/build-binary-assets"
fi

#This list of variables must also be included in the copyenv directive of parsers/include
export CONFIG_DIR="${BASEDIR}/config"
export CHROOT_DIR="${PROJECT_DIR}/chroot"
export PARSERS="${BASEDIR}/parsers"
export SCRIPTS="${BASEDIR}/scripts"
export CALLBACKS="${BASEDIR}/callbacks"

. "${SCRIPTS}/binfmt.sh"
