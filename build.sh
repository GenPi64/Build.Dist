#!/bin/bash

if [[ ! "$UID" == "0" ]]; then
    echo "Build must run as root!"
    exit 1
fi

cd "$(dirname $0)"

source scripts/functions.sh

export BASEDIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

source ${BASEDIR}/env.sh

if [[ ! -d "$PROJECT_DIR" ]]; then
    if [[ ! -e "$PROJECT_DIR" ]]; then
	if [ ! -z $BTRFS_SNAPSHOTS ]; then
	    btrfs subvolume create "$PROJECT_DIR"
	fi
    fi
fi

if [ ! -z $BTRFS_SNAPSHOTS ] ; then
    ckmkdir $BTRFS_SNAPSHOTS
fi

ckmkdir "$PROJECT_DIR"

if test -f "${PROJECT}.json"; then
    $PARSERS/includejson/includejson ${PROJECT}.json
    exit_code=$?
    echo "run complete."
    exit $exit_code
else
    "No ${PROJECT}.json found. Try again."
fi

