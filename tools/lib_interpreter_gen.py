import json
import os
from mako.template import Template

def parse_api(api_path):
    """Parse the API JSON file."""
    with open(api_path, 'r') as api_file:
        return json.load(api_file)

def main():
    base_dir = os.path.dirname(__file__)
    api_path = os.path.normpath(os.path.join(base_dir, '..', 'objects', 'export', 'documentation', 'nislscapi', 'nislscapi_full.json'))
    template_path = os.path.join(base_dir, 'templates/lib_interpreter.py.mako')
    output_path = os.path.join(base_dir, 'lib_interpreter.py')
    try:
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
        if not os.path.exists(api_path):
            raise FileNotFoundError(f"API file not found: {api_path}")

        with open(api_path, 'r') as api_file:
            api = json.load(api_file)

        tpl = Template(filename=template_path)
        rendered = tpl.render(functions=api['functions'], trim_blocks=True, lstrip_blocks=True)

        with open(output_path, 'w') as out_file:
            out_file.write(rendered)
        print(f"Generated Python binding written to {output_path}")

    except Exception as e:
        print(f"Error: {e}")


main()