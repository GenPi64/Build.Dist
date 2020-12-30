#!/bin/bash

echo $PROJECT
if [[ -z "$PROJECT" ]]; then
	export PROJECT="GenPi64"
fi

if [[ -z "$PROJECT_DIR" ]]; then
	export PROJECT_DIR="${BASEDIR}/build/${PROJECT}"
fi

if [[ -z "$BINARY_ASSETS" ]]; then
	export BINARY_ASSETS="${PROJECT_DIR}/build-binary-assets"
fi


echo $PROJECT
#This list of variables must also be included in the copyenv directive of parsers/include
#export PROJECT_DIR="${BASEDIR}/build/${PROJECT}"
export CONFIG_DIR="${BASEDIR}/config"
export CHROOT_DIR="${PROJECT_DIR}/chroot"
export PARSERS="${BASEDIR}/parsers"
export SCRIPTS="${BASEDIR}/scripts"
export CALLBACKS="${BASEDIR}/callbacks"

