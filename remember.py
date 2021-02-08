#!/usr/bin/env python

"""Helps you remember things regularly.

Uses notifications to do so.
"""

import os
import argparse
import logging
import yaml

from rich import print
from notifypy import Notify

http_path = os.path.abspath("http.svg")

parser = argparse.ArgumentParser(prog="remember", description=__doc__)

parser.add_argument("-a", "--add", help="Add an item to remember.")

parser.add_argument(
    "-l",
    "--list",
    action="store_true",
    help="List items to remember.",
)

parser.add_argument(
    "-n",
    "--next",
    action="store_true",
    help="Show the next item to remember.",
)


def notify(message: str):
    """Notify with a given message."""
    notification = Notify(
        default_notification_title="Remember",
        default_application_name="name",
        default_notification_icon=http_path,
        # default_notification_audio=""
    )

    notification.message = message
    notification.send()


def remember(args: argparse.Namespace):
    """Remember a new item."""

    with open("remember.yml", "r") as f:
        content = yaml.safe_load(f)

    if not content:
        content = {}

    if not "list" in content:
        content["list"] = []

    if not "current" in content:
        content["current"] = 0

    if args.add:
        content["list"].append(args.add)

    elif args.next:
        current = content["current"]
        print(content["list"][current])
        content["current"] = (current + 1) % len(content["list"])
        notify(content["list"][current])

    elif args.list:
        print(content["list"])

    with open("remember.yml", "w") as f:
        yaml.dump(content, f)


if __name__ == "__main__":
    args = parser.parse_args()
    remember(args)
