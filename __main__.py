#!/usr/bin/env python

"""
Run expensive background tasks when you're not there
so you won't get mad.
"""

import os
import sys
import yaml
import argparse


parser = argparse.ArgumentParser(
    description="Run expensive tasks when I'm not here.",
    epilog="Have a good time not wasting your time!")

parser.add_argument(
    '-a', '--add', help="Add a task to run later.")
parser.add_argument(
    '-r', '--run', help="Run all tasks of the task list")
parser.add_argument(
    '-s', '--set', nargs=2, help="Set config variables")

args = parser.parse_args()
# args = vars(args)

if args.add:
    print(args.add)

if args.set:
    print(args.set)
