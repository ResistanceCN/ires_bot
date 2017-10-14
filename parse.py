#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import yaml

def parse(path):
    try:
        with open(path, 'r+') as f:
            content = yaml.load(f)
        return content
    except FileNotFoundError:
        print("No such file or directory: " + path)
        sys.exit(1)
    return content

if __name__ == '__main__':
    path = 'example.config.yml'
    config = parse(path)
    print(config['postgres'].keys())
