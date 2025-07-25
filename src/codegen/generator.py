"""Code generation utility for NI SLSC Python API.

This script automates the process of generating Python source files from JSON and XML metadata
using Mako templates. It also copies any handwritten source files to the output directory.
Intended for use in the NI SLSC Python API code generation workflow.
"""

import json
import os
import re
import shutil
import xml.etree.ElementTree as ETree
from pathlib import Path

from mako.template import Template


def _parse_json(json_path: Path) -> dict:
    """Parse the nislscapi JSON file."""
    with open(json_path, "r") as json_file:
        return json.load(json_file)


def _parse_errors(errors_path: Path) -> dict:
    """Parse the errors XML file."""
    errors = []
    errors_xml = ETree.parse(errors_path)
    code_set = set()
    for error in errors_xml.findall("./descriptions/error"):
        code_element = error.find("code")
        code = int(code_element.get("code"))
        symbol = code_element.get("symbol")
        if code in code_set:
            raise RuntimeError(f"Duplicate error code {code} for symbol {symbol}")
        code_set.add(code)
        assert re.match(r"^kError|^kWarning", symbol)
        errors.append({"symbol": symbol, "code": code})
    return errors


def _copy_handwritten_files(source: Path, dest: Path) -> None:
    """Copy handwritten files from source to destination."""
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, dest, dirs_exist_ok=True)


def _generate_code(json: dict, error: dict, source: Path, dest: Path) -> None:
    """Generate code from templates using the provided JSON and XML file provided."""
    for template_file in source.rglob("*.mako"):
        relative_path = template_file.relative_to(source)
        new_dest = dest / relative_path.with_suffix("")
        new_dest.parent.mkdir(parents=True, exist_ok=True)

        with open(template_file, "r", encoding="utf-8") as f:
            template_content = f.read()

        template = Template(template_content)
        context = {**json, "errors": error}
        rendered = template.render(**context)

        with open(new_dest, "w", encoding="utf-8") as f:
            f.write(rendered)


def main() -> None:
    """Coordinate the code generation process.

    Load metadata and error definitions, generates code using templates,
    and copy handwritten files to the output directory.
    """
    parent_dir = Path(__file__).parent.parent.parent
    json_file = parent_dir / "src" / "codegen" / "metadata" / "nislscapi_full.json"
    error_file = parent_dir / "src" / "codegen" / "metadata" / "errors.nimxl"
    template_path = parent_dir / "src" / "codegen" / "templates"
    handwritten_path = parent_dir / "src" / "handwritten"
    destination_path = parent_dir / "generated" / "nislsc"

    if not os.path.exists(json_file):
        raise FileNotFoundError(f"JSON file not found: {json_file}")

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template directory not found: {template_path}")

    if not os.path.exists(handwritten_path):
        raise FileNotFoundError(f"Handwritten directory not found: {handwritten_path}")

    json_data = _parse_json(json_file)

    error_data = _parse_errors(error_file)

    _generate_code(json_data, error_data, template_path, destination_path)

    _copy_handwritten_files(handwritten_path, destination_path)


if __name__ == "__main__":
    main()
