#!/bin/bash
yanglint -f tree \
  -x platform-extension-data.xml \
  -Y platform-toplevel-yanglib.xml \
  -L 69 \
  ietf-platform-manifest@2024-07-02.yang 
