import json
import os
import shutil

from mako.template import Template
from pathlib import Path

def parse_api(api_path):
    """Parse the API JSON file."""
    with open(api_path, 'r') as api_file:
        return json.load(api_file)

def _copy_handwritten_files(dest):
    parent_dir = Path(__file__).parent.parent
    source_path = parent_dir / "handwritten"
    shutil.copytree(source_path, dest, dirs_exist_ok=True)

def generate_from_template(api, template_path, output_path):
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")

    tpl = Template(filename=template_path)
    kwargs = dict(functions=api['functions'], trim_blocks=True, lstrip_blocks=True)
    rendered = tpl.render(**kwargs)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as out_file:
        out_file.write(rendered.encode())
    print(f"Generated Python binding written to {output_path}")

def main():
    base_dir = os.path.dirname(__file__)
    api_path = os.path.normpath(os.path.join(base_dir, 'metadata', 'nislscapi_full.json'))

    if not os.path.exists(api_path):
        raise FileNotFoundError(f"API file not found: {api_path}")

    api = parse_api(api_path)

    targets = [
        {
            "template": os.path.join(base_dir, 'templates', '_base_interpreter.py.mako'),
            "output": os.path.join(base_dir, '..', '..', 'generated', 'nislsc', '_base_interpreter.py'),
        },
        {
            "template": os.path.join(base_dir, 'templates', '_library_interpreter.py.mako'),
            "output": os.path.join(base_dir, '..', '..', 'generated', 'nislsc', '_library_interpreter.py'),
        }
    ]

    for target in targets:
        try:
            generate_from_template(api, target["template"], target["output"])
        except Exception as e:
            print(f"Error generating {target['output']}: {e}")

    _copy_handwritten_files(os.path.join(base_dir, '..', '..', 'generated', 'nislsc'))

if __name__ == "__main__":
    main()