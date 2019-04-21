import argparse
import json
import sys
from collections import MutableMapping
from functools import reduce

import dpath


class Parser(object):
    def __init__(self, data, nesting_levels, **kwargs):
        self.data = data
        self.nesting_levels = nesting_levels
        self.validate()

    def validate(self):
        pass

    def parse(self):
        leaf_names = self.nesting_levels
        result = []
        for item in self.data:
            unused_keys = set(item.keys()).difference(leaf_names)

            leaf_dict = [{key: item.get(key) for key in unused_keys}]

            for name in reversed(leaf_names):
                key = item.get(name)
                leaf_dict = {key: leaf_dict}
            result.append(leaf_dict)

        output = {}
        for item in result:
            dpath.util.merge(output, item)

        return output


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
