#!/usr/bin/env python
"""Helps you remember things regularly.

Uses notifications to do so.
"""

import os
import click
import yaml
import logging
import requests
import dataclasses

# import fastapi

from rich import print
from notifypy import Notify
from dotenv import load_dotenv

from storage import Storage

load_dotenv(".env")
s = Storage(os.environ["MEMO_PATH"])


class Store:
    """CRUD group of va"""

    def __init__(self, key_path: list):
        """Define a crud group of commmands that controls a yaml document
        given."""
        self.key_path = key_path

    def add(self, ):


a = C

# def c
# items = ListSection("items")
# config = DictSection("config")


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
    """Group of commands for configuration."""


@config.command("set")
@click.argument("key", type=str)
@click.argument("value", type=str)
def set(key: str, value: str):
    """Add a new line in config."""
    s.config[key] = value


@config.command(name="get")
@click.argument("key", type=str)
def get(key: str):
    """Add a new line in config."""
    click.echo(s.config[key])


@mem.command(name="add")
@click.argument("item", type=str)
def mem_add(item: str):
    """Add an item to remember."""
    s.items.append(item)
    logging.debug("item_added")
    click.echo("item added")


@mem.command(name="get")
@click.argument("index", type=int)
def mem_get(index: int):
    """Add an item to remember."""
    click.echo(s.items[index])


@mem.command(name="delete")
@click.argument("item", type=str)
def mem_delete(key: str):
    """Delete an item to remember."""
    del s.items[key]
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


if __name__ == "__main__":
    mem()
