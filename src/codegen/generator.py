import json
import os
import shutil

from mako.template import Template
from pathlib import Path

def _parse_json(json_path: Path) -> dict:
    with open(json_path, 'r') as json_file:
        return json.load(json_file)

def _copy_handwritten_files(source: Path, dest: Path) -> None:
    shutil.copytree(source, dest, dirs_exist_ok=True)

def _generate_code(json: dict, source: Path, dest: Path) -> None:
    for template_file in source.iterdir():
        if template_file.suffix == '.mako':
            template_path = template_file
            new_dest = dest / template_file.stem

            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()

            template = Template(template_content)
            rendered = template.render(**json)
            
            with open(new_dest, "w", encoding="utf-8") as f:
                f.write(rendered)

def main() -> None:
    parent_dir = Path(__file__).parent.parent.parent
    json_file = parent_dir / "src" / "codegen" / "metadata" / "nislscapi_full.json"
    template_path = parent_dir / "src" / "codegen" / "templates"
    handwritten_path = parent_dir / "src" / "handwritten"
    destination_path = parent_dir / "generated" / "nislsc"

    if not os.path.exists(json_file):
        raise FileNotFoundError(f"JSON file not found: {json_file}")

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template directory not found: {source_path}")

    if not os.path.exists(handwritten_path):
        raise FileNotFoundError(f"Handwritten directory not found: {handwritten_path}")

    json_data = _parse_json(json_file)

    _generate_code(json_data, template_path, destination_path)

    _copy_handwritten_files(handwritten_path,  destination_path)

if __name__ == "__main__":
    main()