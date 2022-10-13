#!/bin/bash

if [ -f "build/${PROJECT}/${PROJECT}.img" ]; then
  if [ -f "build/${PROJECT}/${PROJECT}-${BUILDVERSION}.img" ]; then
   exit 0
  else
   sudo mv build/${PROJECT}/${PROJECT}.img build/${PROJECT}/${PROJECT}-${BUILDVERSION}.img
   sudo mv build/${PROJECT}/${PROJECT}.img.zst build/${PROJECT}/${PROJECT}-${BUILDVERSION}.img.zst
   sudo mv build/${PROJECT}/${PROJECT}.img.zst.sum build/${PROJECT}/${PROJECT}-${BUILDVERSION}.img.zst.sum
   sudo mv build/${PROJECT}/latest-${PROJECT}.tar.zst build/${PROJECT}/${PROJECT}-${BUILDVERSION}.tar.zst
  fi
fi