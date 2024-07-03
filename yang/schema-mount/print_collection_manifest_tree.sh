#!/bin/bash
yanglint -f tree \
  -x data-manifest-mounted-yl.xml \
  -Y data-manifest-mounter-yl.xml \
  ietf-data-collection-manifest@2024-07-02.yang
