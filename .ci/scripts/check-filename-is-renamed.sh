#!/bin/bash

if [ -f "build/${PROJECT}/${PROJECT}.img" ]; then
    if [ -f "build/${PROJECT}/${PROJECT}-${BUILDVERSION}.img" ]; then
      echo "File build/${PROJECT}/${PROJECT}-${BUILDVERSION}.img exists already so exiting with status 0."
      exit 0
    else
     echo "Processing files..."
     sudo mv build/${PROJECT}/${PROJECT}.img build/${PROJECT}/${PROJECT}-${BUILDVERSION}.img
     sudo mv build/${PROJECT}/${PROJECT}.img.zst build/${PROJECT}/${PROJECT}-${BUILDVERSION}.img.zst
     sudo mv build/${PROJECT}/${PROJECT}.img.zst.sum build/${PROJECT}/${PROJECT}-${BUILDVERSION}.img.zst.sum
     sudo mv build/${PROJECT}/latest-${PROJECT}.tar.zst build/${PROJECT}/${PROJECT}-${BUILDVERSION}.tar.zst
    fi
  else
    echo "File build/${PROJECT}/${PROJECT}.img doesn't exist, exiting"
fi