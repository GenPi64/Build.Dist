#!/bin/bash
export BASEDIR=${PWD}

if [[ -z "$PROJECT" ]]; then
	export PROJECT="GenPi64"
fi

if [[ -z "$PROJECT_DIR" ]]; then
	export PROJECT_DIR="${BASEDIR}/build/${PROJECT}"
fi

#This list of variables must also be included in the copyenv directive of parsers/include
export CONFIG_DIR="${BASEDIR}/config"
export CHROOT_DIR="${PROJECT_DIR}/chroot"
export PARSERS="${BASEDIR}/parsers"
export BINARY_ASSETS="${BASEDIR}/build-binary-assets"
export SCRIPTS="${BASEDIR}/scripts"
export CALLBACKS="${BASEDIR}/callbacks"
