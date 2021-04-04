#!/usr/bin/env python

"""Fetch a file on the website of Marc Partensky."""

import os
import requests
import argparse
import yaml
import pyperclip
import logging

from rich import print

CONFIG_PATH = os.path.abspath(
    os.path.join(os.environ["PROGRAMS_PATH"], "automation", "share.yml")
)

with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument("url", help="url to fetch")
parser.add_argument("filename", nargs="?", help="filename to download to")

parser.add_argument(
    "-t",
    "--token",
    nargs="?",
    default=config["token"],
    help="token for authentication",
)

args = parser.parse_args()


def fetch(url: str, token: str = None, filename: str = None):
    """Fetch a file with restricted access."""
    session = requests.Session()
    response = session.get(url, params=dict(token=token), allow_redirects=True)

    print(response)
    if response.status_code != 200:
        text = "".join(("[bold red]", response.reason, "[/bold red]: ", response.text))
        print(text)
        return response

    if not filename:
        filename = (
            response.headers["Content-Disposition"]
            .split(";")[1]
            .strip()
            .replace("filename=", "")
            .replace('"', "")
        )

    path = os.path.join(os.getcwd(), filename)

    with open(path, "w") as f:
        f.write(response.text)

    try:
        pyperclip.copy(path)
        print(
            "[bold green]Success[/bold green]: "
            f"downloaded to '[italic magenta]{path}[/italic magenta]' "
            "and [bold]copied path[/bold] to clipboard."
        )
    except:
        print(
            "[bold green]Success[/bold green]: "
            f"downloaded to '[italic magenta]{path}[/italic magenta]' "
        )
        logging.warning("Could not copy path to clipboard.")


if __name__ == "__main__":
    fetch(url=args.url, token=args.token, filename=args.filename)
