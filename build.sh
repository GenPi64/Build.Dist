#! /bin/bash

if [[ ! "$UID" == "0" ]]; then
    echo "Build must run as root!"
    exit 1
fi

cd "$(dirname $0)"

source scripts/functions.sh

export BASEDIR=${PWD}

source ${BASEDIR}/env.sh



ckmkdir "$PROJECT_DIR"

if test -f "${PROJECT}.json"; then
    $PARSERS/includejson/includejson ${PROJECT}.json
    echo "run complete."
else
    "No ${PROJECT}.json found. Try again."
fi

