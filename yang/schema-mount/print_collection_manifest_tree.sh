#!/bin/bash
yanglint -f tree \
  -x data-collection-extension-data.xml \
  -Y data-collection-toplevel-yanglib.xml \
  -L 69 \
  ietf-data-collection-manifest@2024-07-02.yang
