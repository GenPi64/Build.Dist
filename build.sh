#! /bin/bash

if [[ ! "$UID" == "0" ]]; then
    echo "Build must run as root!"
    exit 1
fi

cd "$(dirname $0)"

source scripts/functions.sh

source env.sh



ckmkdir "$PROJECT_DIR"

if test -f "${PROJECT}.json"; then
    $PARSERS/includejson/includejson ${PROJECT}.json
else
    $PARSERS/include/include ${PROJECT}.manifest
fi

echo "run complete."
