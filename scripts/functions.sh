#!/bin/bash
# This script is meant to be sourced only; not run directly

systemctl_enable () {
    action="${2}"
    echo "systemctl ${action} ${1}"
}

rcupdate_add () {
    echo "rc-update add ${1} ${2}"
}

ckmkdir () {
if [[ ! -d "${1}" ]]; then
  if [[ ! -e "${1}" ]]; then
    mkdir -p "${1}"
  fi
fi

}

copyconf () {
pushd "$(dirname "${0}")" || exit 80

if [[ -z "${2}" ]]; then
  U="root"
else
  U="${2}"
fi

if [[ -z "${3}" ]]; then
  G="root"
else
  G=${3}
fi

for ITEM in "${PROJECT}"/*
do
  [[ -e "${ITEM}" ]] || break  # Handle the case of empty PROJECT
  
  if [[ -d "${PROJECT}/${ITEM}" ]]; then
    mkdir -p "${PROJECT_DIR}"/chroot/"${1}"/"${ITEM}"
    for ITEM2 in "${PROJECT}"/"${ITEM}"/*
        do
            [[ -e "${ITEM2}" ]] || break  # Handle the case of empty PROJECT/ITEM
            cp -r "${PROJECT}"/"${ITEM}"/"${ITEM2}" "${PROJECT_DIR}"/chroot/"${1}"/"${ITEM}"/"${ITEM2}"
            chown "${U}":"${G}" "${PROJECT_DIR}"/chroot/"${1}"/"${ITEM}"/"${ITEM2}"
        done
  else
    cp -r "${PROJECT}"/"${ITEM}" "${PROJECT_DIR}"/chroot/"${1}"/"${ITEM}"
    chown "${U}":"${G}" "${PROJECT_DIR}"/chroot/"${1}"/"${ITEM}"
  fi
done

popd || exit 81

}
