#!/bin/bash

# Set environment variables
export PROJECT="GenPi64Systemd"
export CCACHE_DIR="${HOME}/shared/ccache"
export BINPKGS_DIR="${HOME}/shared/binpkgs"
export DISTFILES_DIR="${HOME}/shared/distfiles"
export OVERLAYS_CACHE_DIR="${HOME}/shared/overlays-cache"
export BINARY_ASSETS="${HOME}/shared/binary_assets"
export NO_PARALLEL="yes"

# Print the variables for verification
echo "PROJECT: $PROJECT"
echo "CCACHE_DIR: $CCACHE_DIR"
echo "BINPKGS_DIR: $BINPKGS_DIR"
echo "DISTFILES_DIR: $DISTFILES_DIR"
echo "OVERLAYS_CACHE_DIR: $OVERLAYS_CACHE_DIR"
echo "BINARY_ASSETS: $BINARY_ASSETS"
echo "NO_PARALLEL: $NO_PARALLEL"
