all:
	cd builder; python3 build_data_manifest_draft.py
	CURRENT_VERSION=$$(ls draft-ietf-opsawg-collected-data-manifest-??.xml | sort | tail -n 1);\
	echo "CURRENT_VERSION=$$CURRENT_VERSION"; \
	LOCALE="LANG_C" xml2rfc --v2 $$CURRENT_VERSION; \
	PREVIOUS_VERSION=$$(ls draft-ietf-opsawg-collected-data-manifest-??.xml | sort | tail -n 2 | head -n 1); \
	rfcdiff $$(basename $$PREVIOUS_VERSION .xml).txt $$(basename $$CURRENT_VERSION .xml).txt

