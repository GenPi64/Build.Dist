#! /bin/bash

if [[ ! "$UID" == "0" ]]; then
    echo "Build must run as root!"
    exit 1
fi

cd "$(dirname $0)"

source scripts/functions.sh

export BASEDIR=$(pwd)
export CONFIG_DIR=$(pwd)/config

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
export CHROOT_DIR="$PROJECT_DIR/chroot"
export PARSERS="${BASEDIR}/parsers"
export BINARY_ASSETS="${BASEDIR}/build-binary-assets"
export SCRIPTS="$BASEDIR/scripts"
export CALLBACKS="$BASEDIR/callbacks"


ckmkdir "$PROJECT_DIR"

if test -f "${PROJECT}.json"; then
    $PARSERS/includejson/includejson ${PROJECT}.json
else
    $PARSERS/include/include ${PROJECT}.manifest
fi

echo "run complete."
