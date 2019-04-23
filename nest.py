import argparse
import json
import os
import sys
import textwrap

from app.utils.parser import Parser

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main(data, nesting_levels):
    p = Parser(data, nesting_levels)
    output = p.parse()
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":

    help_text = textwrap.dedent('''
        Usage: 
                 cat example_input.json | python nest.py currency country city
                 python nest.py --file input.json currency country city
    ''')

    parser = argparse.ArgumentParser(
        description='Parse JSON file',
        epilog=help_text,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('levels',
                        type=str,
                        nargs='*',
                        help='nesting levels for the dict')
    parser.add_argument('--file',
                        nargs='?',
                        type=argparse.FileType('rb'),
                        default=sys.stdin)

    args = parser.parse_args(sys.argv[1:])

    data = args.file.detach().read(
    ) if args.file.name == '<stdin>' else args.file.read()

    nesting_levels = args.levels

    main(json.loads(data), nesting_levels)
