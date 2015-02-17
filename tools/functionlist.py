#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import ast
import sys
import os

import yaml

sys.path.insert(0, os.getcwd())

from py2cpp.util.function import function_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", "-o", nargs="?",
                        type=argparse.FileType("w"), default=sys.stdout)

    args = parser.parse_args()

    data = {}
    for path,names,files in os.walk(args.input):
        for file in files:
            root,ext = os.path.splitext(file)
            if ext != '.py':
                continue
            filepath = os.path.join(path, file)
            src = open(filepath).read()
            node = ast.parse(src, filepath)
            result = function_list(node)
            if result:
                data[filepath] = result

    serialized = yaml.dump(data, allow_unicode=True, default_flow_style=False)
    args.output.write(serialized)

    return 0

if __name__ == '__main__':
    sys.exit(main())
