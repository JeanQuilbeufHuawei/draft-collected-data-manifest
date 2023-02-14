# Data Manifest for Streaming Telemetry

This repo contains the draft for the next version of
[draft-claise-opsawg-collected-data-manifest](https://datatracker.ietf.org/doc/draft-claise-opsawg-collected-data-manifest/)


[Diff between this repo and latest ietf
version](http://tools.ietf.org//rfcdiff?url1=https://www.ietf.org/archive/id/draft-claise-opsawg-collected-data-manifest-05.txt&url2=https://raw.githubusercontent.com/JeanQuilbeufHuawei/draft-collected-data-manifest/master/draft-claise-opsawg-collected-data-manifest-06.txt)

## Modifying the draft

### Quick way

Modify the .xml corresponding to the current version. Make sure to 
commit the corresponding .txt so that diff with current version is correct.

### Automated way (Preferred if YANG modules are modified)

#### Dependencies

 * python3
 * make
 * xml2rfc
 * pip

Python dependencies are listed in [builder/requirements.txt](builder/requirements.txt).
Install them  with `pip install -r builder/requirements.txt`

#### Modifying and building

The text of the draft can be modified in [builder/draft-claise-opsawg-collected-data-manifest.xml](builder/draft-claise-opsawg-collected-data-manifest.xml)

The YANG modules are in the [yang](yang) directory.

Use `make` to build the .xml and .txt of the draft.

:warning: This will overwrite the latest version of the draft in the current directory (e.g. if modified with the quick way above).

The makefile at the root of this repository will check the YANG files 
for errors and assemble them into a complete xml file and generate the .txt.





