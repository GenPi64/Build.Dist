#! /bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

. ${SCRIPT_DIR}/env.sh
${SCRIPT_DIR}/scripts/chroot.py
