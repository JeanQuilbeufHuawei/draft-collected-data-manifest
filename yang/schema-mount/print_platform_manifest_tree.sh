#!/bin/bash
yanglint -f tree \
  -x platform-extension-data.xml \
  -Y platform-toplevel-yanglib.xml \
  -L 69 \
  ietf-platform-manifest@2025-02-21.yang 
