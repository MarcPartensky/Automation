#!/usr/bin/env python
"""Helps you remember things regularly.

Uses notifications to do so.
"""

import os
import logging
import click
import yaml
import logging

from rich import print
from notifypy import Notify
from dotenv import load_dotenv

from storage import Storage

load_dotenv(".env")
s = Storage(os.environ["MEMO_PATH"])


def notify(message: str):
    """Notify with a given message."""
    notification = Notify(
        default_notification_title="Remember",
        default_application_name="name",
        default_notification_icon=s.config.http_path,
        # default_notification_audio=""
    )

    notification.message = message
    notification.send()


@click.group()
def mem():
    """Define a new group of commands."""


@mem.group()
def config():
    """Group of comands for configuration."""


@config.command("set")
@click.argument("key", type=str)
@click.argument("value", type=str)
def config_set(key: str, value: str):
    """Add a new line in config."""
    s.config[key] = value


@config.command(name="get")
@click.argument("key", type=str)
def config_get(key: str):
    """Add a new line in config."""
    click.echo(s.config[key])


@mem.command(name="add")
@click.argument("item", type=str)
def mem_add(item: str):
    """Add an item to remember."""
    s.items.append(item)
    click.echo("item added")


@mem.command(name="delete")
@click.argument("item", type=str)
def mem_delete():
    """Delete an item to remember."""
    click.echo("delete")


@mem.command(name="notify")
def mem_notify():
    """Notify with an item to remember"""
    notify("test")
    click.echo("notify")


@mem.command(name="list")
def mem_list():
    """List items to remember"""
    for item in s.items:
        click.echo(item)


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
