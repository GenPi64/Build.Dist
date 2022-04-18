#!/bin/bash

if [[ ! "${UID}" == "0" ]]; then
    echo "Build must run as root!"
    exit 1
fi

cd "$(dirname "${0}")" || exit

source scripts/functions.sh

# Presumes the PWD variable has been set the calling shell
export BASEDIR="${PWD}"

source "${BASEDIR}"/env.sh

if [[ ! -d "${PROJECT_DIR}" ]]; then
    if [[ ! -e "$PROJECT_DIR" ]]; then
	if [ -n "${BTRFS_SNAPSHOTS}" ]; then
	    btrfs subvolume create "${PROJECT_DIR}"
	fi
    fi
fi

if [ -n "${BTRFS_SNAPSHOTS}" ] ; then
    ckmkdir "${BTRFS_SNAPSHOTS}"
fi

ckmkdir "${PROJECT_DIR}"

if test -f "${PROJECT}.json"; then
    "${PARSERS}/includejson/includejson" "${PROJECT}.json"
    echo "run complete."
else
    echo "No ${PROJECT}.json found. Try again."
fi

