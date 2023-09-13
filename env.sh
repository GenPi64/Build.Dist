#!/bin/bash
export BASEDIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

if [ -z "$PROJECT" ]; then
	export PROJECT="GenPi64OpenRC"
fi

if [ -z "$PROJECT_DIR" ]; then
	export PROJECT_DIR="${BASEDIR}/build/${PROJECT}"
fi

if [ -z "$BINPKGS_DIR" ] ; then
        export BINPKGS_DIR="${PROJECT_DIR}/packages"
fi

if [ -z "$DISTFILES_DIR" ] ; then
        export DISTFILES_DIR="${PROJECT_DIR}/distfiles"
fi

if [ -z "$CCACHE_DIR" ]; then
	export CCACHE_DIR="${PROJECT_DIR}/ccache"
fi

if [ -z "$BINARY_ASSETS" ]; then
	export BINARY_ASSETS="${PROJECT_DIR}/build-binary-assets"
fi

if [ -z "$OVERLAYS_CACHE_DIR" ]; then
	export OVERLAYS_CACHE_DIR="${PROJECT_DIR}/overlays-cache"
fi

#This list of variables must also be included in the copyenv directive of parsers/include
export CONFIG_DIR="${BASEDIR}/config"
export CHROOT_DIR="${PROJECT_DIR}/chroot"
export PARSERS="${BASEDIR}/parsers"
export SCRIPTS="${BASEDIR}/scripts"
export CALLBACKS="${BASEDIR}/callbacks"

. "${SCRIPTS}/binfmt.sh"
