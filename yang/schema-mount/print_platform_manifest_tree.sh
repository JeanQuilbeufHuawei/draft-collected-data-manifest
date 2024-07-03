#!/bin/bash
yanglint -f tree \
  -x platform-manifest-mounted-yl.xml \
  -Y platform-manifest-mounter-yl.xml \
  ietf-platform-manifest@2024-07-02.yang 
