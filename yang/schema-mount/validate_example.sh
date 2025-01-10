#!/bin/bash

yanglint -e -f xml -x data-collection-extension-data.xml -Y data-collection-toplevel-yanglib.xml ../../json/manifests-example.json
