import json
import os
import re
import shutil

import xml.etree.ElementTree as ETree
from mako.template import Template
from pathlib import Path

def _parse_json(json_path: Path) -> dict:
    with open(json_path, 'r') as json_file:
        return json.load(json_file)

def _parse_errors(errors_path: Path) -> dict:
    """Parse the errors XML file."""
    errors = []
    errors_xml = ETree.parse(errors_path)
    code_set = set()
    for error in errors_xml.findall('./descriptions/error'):
        code_element = error.find('code')
        code = int(code_element.get('code'))
        symbol = code_element.get('symbol')
        if code in code_set:
            raise RuntimeError('Duplicate error code {0} for symbol {1}'.format(code, symbol))
        code_set.add(code)
        assert re.match(r'^kError|^kWarning', symbol)
        errors.append({
            'symbol': symbol,
            'code': code
        })
    return errors

def _copy_handwritten_files(source: Path, dest: Path) -> None:
    shutil.copytree(source, dest, dirs_exist_ok=True)

def _generate_code(json: dict, error: dict, source: Path, dest: Path) -> None:
    for template_file in source.iterdir():
        if template_file.suffix == '.mako':
            template_path = template_file
            new_dest = dest / template_file.stem

            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()

            template = Template(template_content)
            context = {**json, "errors": error}
            rendered = template.render(**context)

            with open(new_dest, "w", encoding="utf-8") as f:
                f.write(rendered)

def main() -> None:
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

    _copy_handwritten_files(handwritten_path,  destination_path)

if __name__ == "__main__":
    main()
