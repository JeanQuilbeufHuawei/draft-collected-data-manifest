all:
	cd builder; python3 build_data_manifest_draft.py
	LOCALE="EN_us.utf8" xml2rfc --v2 draft-claise-opsawg-collected-data-manifest-??.xml

