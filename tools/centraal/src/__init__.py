import argparse
import importlib.util

parser = argparse.ArgumentParser(
    description='Centraal CLI to manage clusters and services.')
parser.add_argument('tool', choices=[
    'master'
])
parser.add_argument('subtool')

if __name__ == "__main__":

    args, unknown = parser.parse_known_args()
    tool = args.tool
    subtool = args.subtool

    spec = importlib.util.spec_from_file_location(
        name=tool + '.' + subtool,
        location='src/' + tool + '/' + subtool + '.py',
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
