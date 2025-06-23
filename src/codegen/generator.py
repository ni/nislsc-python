import json
import os
<<<<<<< HEAD
import shutil

from mako.template import Template
from pathlib import Path
=======
from mako.template import Template
>>>>>>> 168e9ca8d84a4e2b7038150811b9de9ae95d5d4e

def parse_api(api_path):
    """Parse the API JSON file."""
    with open(api_path, 'r') as api_file:
        return json.load(api_file)

<<<<<<< HEAD
def _copy_handwritten_files(dest):
    parent_dir = Path(__file__).parent.parent
    source_path = parent_dir / "handwritten"
    shutil.copytree(source_path, dest, dirs_exist_ok=True)

def generate_from_template(api, template_path, output_path, context):
=======
def generate_from_template(api, template_path, output_path):
>>>>>>> 168e9ca8d84a4e2b7038150811b9de9ae95d5d4e
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")

    tpl = Template(filename=template_path)
<<<<<<< HEAD
    kwargs = dict(trim_blocks=True, lstrip_blocks=True)

    if context == 'functions':
        kwargs['functions'] = api['functions']
    elif context == 'enums':
        kwargs['enums'] = api['enums']

    rendered = tpl.render(**kwargs)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as out_file:
        out_file.write(rendered.encode())
=======
    kwargs = dict(functions=api['functions'], trim_blocks=True, lstrip_blocks=True)
    rendered = tpl.render(**kwargs)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as out_file:
        out_file.write(rendered)
>>>>>>> 168e9ca8d84a4e2b7038150811b9de9ae95d5d4e
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
<<<<<<< HEAD
            "context": "functions",
=======
>>>>>>> 168e9ca8d84a4e2b7038150811b9de9ae95d5d4e
        },
        {
            "template": os.path.join(base_dir, 'templates', '_library_interpreter.py.mako'),
            "output": os.path.join(base_dir, '..', '..', 'generated', 'nislsc', '_library_interpreter.py'),
<<<<<<< HEAD
            "context": "functions",
        },
        {
            "template": os.path.join(base_dir, 'templates', 'constants.py.mako'),
            "output": os.path.join(base_dir, '..', '..', 'generated', 'nislsc', 'constants.py'),
            "context": "enums",
=======
>>>>>>> 168e9ca8d84a4e2b7038150811b9de9ae95d5d4e
        }
    ]

    for target in targets:
        try:
<<<<<<< HEAD
            generate_from_template(api, target["template"], target["output"], target["context"])
        except Exception as e:
            print(f"Error generating {target['output']}: {e}")

    _copy_handwritten_files(os.path.join(base_dir, '..', '..', 'generated', 'nislsc'))

=======
            generate_from_template(api, target["template"], target["output"])
        except Exception as e:
            print(f"Error generating {target['output']}: {e}")

>>>>>>> 168e9ca8d84a4e2b7038150811b9de9ae95d5d4e
if __name__ == "__main__":
    main()