import json
import os.path
import subprocess
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape

BUILDER_DIR = os.path.dirname(os.path.abspath(__file__))
YANG_DIR = os.path.join(os.path.dirname(BUILDER_DIR), "yang")
JSON_DIR = os.path.join(os.path.dirname(BUILDER_DIR), "json")


env = Environment(
    loader=FileSystemLoader(BUILDER_DIR),
    autoescape=select_autoescape("xml")
)


def _execute_pyang(options: List[str], filenames: List[str]):
    options += ["-p", YANG_DIR]
    args = ["pyang"] + options + filenames
    result = subprocess.run(args, capture_output=True, text=True)
    print()
    print("******************************************************")
    print(" ".join(args))
    print("******************************************************")
    print(" ERRORS ")
    print(result.stderr)
    print("******************************************************")
    print(" OUT ")
    print(result.stdout)
    print("******************************************************")
    return result.stderr, result.stdout


def _build_tree(filenames):
    return _execute_pyang(["-f", "tree", "--tree-line-length", "67"], filenames)


def _format_yang(filenames):
    return _execute_pyang(["--ietf", "-f", "yang",
                           "--yang-canonical",
                           "--yang-line-length", "69"], filenames)


def _find_yang_file(prefix: str, schema_mount=False):
    if schema_mount:
        yang_dir = os.path.join(YANG_DIR, "schema-mount")
    else:
        yang_dir = YANG_DIR
    for yang_file in os.listdir(yang_dir):
        if yang_file.startswith(prefix + "@") and yang_file.endswith("yang"):
            return os.path.join(yang_dir, yang_file)
    raise Exception(f"Yang file with prefix {prefix} not found.")


def _format_json(filename):
    try:
        #return "", json.dumps(json.load(open(filename)), indent=2)
        return "", open(filename).read()
    except Exception as e:
        return str(e), ""


def _get_sm_xml(short_name):
    filename = os.path.join(YANG_DIR, "schema-mount", short_name + ".xml")
    return "", open(filename).read()

def _get_tree(short_name):
    filename = os.path.join(YANG_DIR, "schema-mount", short_name + ".tree")
    return "", open(filename).read()


PLATFORM_MANIFEST_SM = _find_yang_file("ietf-platform-manifest", schema_mount=True)
DATA_COLLECTION_STATS = _find_yang_file("ietf-yp-current-period", schema_mount=True)
DATA_COLLECTION_MANIFEST_SM = _find_yang_file( "example-collection-manifest",
                                               schema_mount=True)
DATA_COLLECTION_MANIFEST_EXAMPLE = os.path.join(JSON_DIR, "manifests-example.json")


def draft_content():
    pyang_results = {
        "data_collection_manifest_tree": _get_tree( "data_collection_manifest"),  # _build_tree([ DATA_COLLECTION_MANIFEST]),
        "data_collection_manifest_yang": _format_yang([DATA_COLLECTION_MANIFEST_SM]),
        "data_collection_manifest_statistics": _format_yang([DATA_COLLECTION_STATS]),
        "platform_manifest_tree": _build_tree([PLATFORM_MANIFEST_SM]),
        #_build_tree([PLATFORM_MANIFEST]),
        #"platform_manifest_yang": _format_yang([PLATFORM_MANIFEST]),
        "data_collection_manifest_example": _format_json(DATA_COLLECTION_MANIFEST_EXAMPLE),
        "platform_schema_mount": _format_yang([PLATFORM_MANIFEST_SM]),
        "platform_extension_data": _get_sm_xml("platform-extension-data"),
        "platform_toplevel_yanglib": _get_sm_xml("platform-toplevel-yanglib"),
        "data_schema_mount": _format_yang([DATA_COLLECTION_MANIFEST_SM]),
        "data_extension_data": _get_sm_xml("data-collection-extension-data"),
        "data_toplevel_yanglib": _get_sm_xml( "data-collection-toplevel-yanglib"),
        "current_period_tree": _build_tree([DATA_COLLECTION_STATS])
        }
    errors = []
    warnings = []
    contents = {}
    for key, (error, output) in pyang_results.items():
        contents[key] = output.strip()
        if error != "":
            for issue in error.splitlines():
                if issue == "":
                    continue
                if issue.split(":")[2] == " warning":
                    warnings.append(issue)
                else:
                    errors.append(issue)
    if warnings:
        print("************WARNINGS******************")
        for error in warnings:
            print(error)
    if errors:
        print("************ERRORS********************")
        for error in errors:
            print(error)
        exit(1)
    return contents


if __name__ == '__main__':
    output = os.path.join(os.path.dirname(BUILDER_DIR), "draft-ietf-opsawg-collected-data-manifest-06.xml")
    draft_text = env.get_template("draft-claise-opsawg-collected-data-manifest.xml")
    with open(output, 'w') as xml_generated:
        xml_generated.write(draft_text.render(**draft_content()))
