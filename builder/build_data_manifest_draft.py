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
    return _execute_pyang(["-f", "tree", "--tree-line-length", "69"], filenames)


def _format_yang(filenames):
    return _execute_pyang(["--ietf", "-f", "yang",
                           "--yang-canonical",
                           "--yang-line-length", "69"], filenames)


def _find_yang_file(prefix: str):
    for yang_file in os.listdir(YANG_DIR):
        if yang_file.startswith(prefix) and yang_file.endswith("yang"):
            return os.path.join(YANG_DIR, yang_file)
    raise Exception(f"Yang file with prefix {prefix} not found.")


def _format_json(filename):
    try:
        #return "", json.dumps(json.load(open(filename)), indent=2)
        return "", open(filename).read()
    except Exception as e:
        return str(e), ""


PLATFORM_MANIFEST = _find_yang_file("ietf-platform-manifest")
DATA_COLLECTION_MANIFEST = _find_yang_file("ietf-data-collection-manifest")
YANG_PUSH_MODIF = _find_yang_file("ietf-yang-push-modif")
DATA_COLLECTION_MANIFEST_EXAMPLE = os.path.join(JSON_DIR, "manifests-example.json")


def draft_content():
    pyang_results = {
        "data_collection_manifest_tree": _build_tree([DATA_COLLECTION_MANIFEST]),
        "data_collection_manifest_yang": _format_yang([DATA_COLLECTION_MANIFEST]),
        "platform_manifest_tree": _build_tree([PLATFORM_MANIFEST]),
        "platform_manifest_yang": _format_yang([PLATFORM_MANIFEST]),
        "data_collection_manifest_example": _format_json(DATA_COLLECTION_MANIFEST_EXAMPLE),
        "yp_modif": _format_yang([YANG_PUSH_MODIF])
        }
    errors = []
    contents = {}
    for key, (error, output) in pyang_results.items():
        contents[key] = output.strip()
        if error != "":
            errors.append(key + "\n" + error)
    if errors:
        for error in errors:
            print("************ERROR********************")
            print(error)
        exit(1)
    return contents


if __name__ == '__main__':
    output = os.path.join(os.path.dirname(BUILDER_DIR), "draft-ietf-opsawg-collected-data-manifest-04.xml")
    draft_text = env.get_template("draft-claise-opsawg-collected-data-manifest.xml")
    with open(output, 'w') as xml_generated:
        xml_generated.write(draft_text.render(**draft_content()))
