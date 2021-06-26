#!/usr/bin/env python
"""Helps you remember things regularly.

Uses notifications to do so.
"""

import os
import logging
import click
import yaml

from rich import print

from notifypy import Notify

http_path = "/Users/marcpartensky/Programs/Automation/http.svg"


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


@click.group()
def mem():
    """Define a new group of commands."""


@mem.command()
@click.argument("item", type=str)
def add(item: str):
    """Add an item to remember."""

    click.echo("item added")


@mem.command()
@click.argument("item", type=str)
def delete():
    """Delete an item to remember."""
    click.echo("delete")


@mem.command(name="notify")
def notify_():
    """Notify with an item to remember"""
    notify("test")
    click.echo("notify")


@mem.command(name="list")
def list_():
    """List items to remember"""
    click.echo("notify")


# def remember(args: argparse.Namespace):
#     """Remember a new item."""

#     with open("remember.yml", "r") as f:
#         content = yaml.safe_load(f)

#     print(args)

#     if not content:
#         content = {}

#     if not "list" in content:
#         content["list"] = []

#     if not "current" in content:
#         content["current"] = 0

#     if args.add:
#         content["list"].append(args.add)

#     if args.delete:
#         del content["list"][args.delete]

#     elif args.next:
#         current = content["current"]
#         print(content["list"][current])
#         content["current"] = (current + 1) % len(content["list"])
#         notify(content["list"][current])

#     elif args.list:
#         print(list(enumerate(content["list"])))

#     with open("remember.yml", "w") as f:
#         yaml.dump(content, f)


# if __name__ == "__main__":
#     if not os.path.exists("remember.yml"):
#         print("No [bold]remember.yml[/bold] file found. Creating one instead.")
#         open("remember.yml").close()
#     args = parser.parse_args()
#     remember(args)

if __name__ == "__main__":
    mem()
