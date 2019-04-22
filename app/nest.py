import argparse
import json
import sys
from collections import MutableMapping
from functools import reduce

from app.utils.parser import Parser


def main(data, nesting_levels):
    p = Parser(data, nesting_levels)
    output = p.parse()
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('levels', type=str, nargs='*')
    parser.add_argument('--file',
                        nargs='?',
                        type=argparse.FileType('rb'),
                        default=sys.stdin)

    args = parser.parse_args(sys.argv[1:])

    data = args.file.detach().read()
    nesting_levels = args.levels

    main(json.loads(data), nesting_levels)
