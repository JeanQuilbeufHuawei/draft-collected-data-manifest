import os.path
import subprocess
from typing import List

from jinja2 import Environment, select_autoescape, FileSystemLoader

BUILDER_DIR = os.path.dirname(__file__)
YANG_DIR = os.path.join(os.path.dirname(BUILDER_DIR), "yang")

env = Environment(
    loader=FileSystemLoader(BUILDER_DIR),
    autoescape=select_autoescape("xml")
)


def _execute_pyang(options: List[str], filenames: List[str]) -> str:
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
    return result.stdout


def _build_tree(filenames):
    return _execute_pyang(["-f", "tree"], filenames)


def _format_yang(filenames):
    return _execute_pyang(["-f", "yang"], filenames)


def _find_yang_file(prefix: str):
    for yang_file in os.listdir(YANG_DIR):
        if yang_file.startswith(prefix) and yang_file.endswith("yang"):
            return os.path.join(YANG_DIR, yang_file)
    raise Exception(f"Yang file with prefix {prefix} not found.")


PLATFORM_MANIFEST = _find_yang_file("ietf-collected-data-platform")
DATA_MANIFEST = _find_yang_file("ietf-collected-data-manifest")


def draft_content():
    return {
        "data_manifest_tree": _build_tree([DATA_MANIFEST]),
        "data_manifest_yang": _format_yang([DATA_MANIFEST]),
        "platform_manifest_tree": _build_tree([PLATFORM_MANIFEST]),
        "platform_manifest_yang": _format_yang([PLATFORM_MANIFEST]),
        }


if __name__ == '__main__':
    output = os.path.join(os.path.dirname(BUILDER_DIR), "draft-claise-opsawg-collected-data-manifest-01.xml")
    draft_text = env.get_template("draft-claise-opsawg-collected-data-manifest.xml")
    with open(output, 'w') as xml_generated:
        xml_generated.write(draft_text.render(**draft_content()))