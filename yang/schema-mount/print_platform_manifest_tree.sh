#!/bin/bash
yanglint -f tree \
  -x platform-extension-data.xml \
  -Y platform-toplevel-yanglib.xml \
  ietf-platform-manifest@2024-07-02.yang 
