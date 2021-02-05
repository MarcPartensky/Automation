#!/usr/bin/env python

"""
Find yaml files with specific names (e.g `commands.yml`, `Procfile`) and make local
commands out of them.
"""

import argparse
import sys
import os
import yaml

from subprocess import call
from rich import print

files = [
    'commands.yml',
    'Procfile'
]

def build_parser():
    """Return a an argparse parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--file', '-f', nargs='+', type=str, default=files,
        help='Manually provide a file containing commands.')

    # parser.
    return parser

def main(argv:list, parser:argparse.ArgumentParser, files:list=[]):
    """Main function."""
    # args = parser.parse_args(argv)
    # if len(sys.argv)==1:
    #     print("[bold]No command[\bold] given as input.")
    listdir = os.listdir()
    found = 0
    for file in files:
        if file in listdir:
            load(file)
            found += 1
    if not found:
        print(f"[bold]No file[/bold] found in \
              [bold]{os.getcwd()}[/bold]!")


def load(file):
    """Load a specific file"""

    with open(file) as f:
        commands = yaml.load(f, Loader=yaml.FullLoader)

    for alias, command in commands.items():
        # call(f'alias {alias}="{command}"')
        os.system(f'alias {alias}="{command}"')

    # if not command in commands:
    #     print(f"Command [bold]{command}[\bold] does not exist.")

    # code = commands[command]
    # os.system(code)

if __name__ == "__main__":
    parser = build_parser()
    main(sys.argv, parser, files)
