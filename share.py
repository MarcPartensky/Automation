#!/usr/bin/env python

"""
Share a file on the website of Marc Partensky
and send back a link to access it.
"""


import os
import argparse
import requests
import logging
import yaml
import certifi
import pyperclip
import logging

from rich import print


CONFIG_PATH = os.path.abspath(
    os.path.join(os.environ["PROGRAMS_PATH"], "automation", "share.yml")
)

with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

if not config:
    logging.info("Config file path not found. Falling back to default config.")
    config = dict(url=[os.environ["WEBSITE_URL"]])

logging.info(f"config: {config}")

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument("file", help="file to share.")

parser.add_argument(
    "-t",
    "--token",
    nargs="?",
    default=config["token"],
    help="token for authentication",
)

parser.add_argument(
    "-u", "--url", dest="urls", nargs="+", default=config["url"], help="website url"
)

parser.add_argument(
    "-m", "--method", nargs="?", default=config["method"], help="http method"
)

parser.add_argument(
    "-p", "--public", nargs="?", default=config["public"], help="http method"
)

parser.add_argument(
    "--perm",
    "--permission",
    dest="permissions",
    nargs="*",
    default=config["permission"],
    help="http method",
)
# parser.add_argument("-c", "--config", default=config, help="default config filepath.")

parser.add_argument(
    "-c",
    "--cert",
    nargs="?",
    default=config["cert"] or certifi.where(),
    help="tls/ssl certificate path",
)


def share_file(
    file: str,
    urls: list = [],
    method: str = "POST",
    token: str = None,
    cert: str = None,
    public: bool = None,
):
    """Share a file using a website."""
    path = os.path.abspath(file)
    file = file.replace("./", "").split("/")[-1]

    with open(path, "rb") as f:
        content = f.read()

    # check for empty file
    # content = "\n".join(content[1:]).strip()
    if content == b"":
        raise Exception("This file is empty!")

    raw_files = {"file": (file, content)}
    session = requests.Session()

    for url in urls:
        url = url.replace("http://", "").replace("https://", "")
        logging.info(f"Sending file to {url}.")

        if cert:
            protocol = "https"
        else:
            protocol = "http"

        full_url = f"{protocol}://{url}/f"
        print(full_url)

        response = session.post(
            url=full_url,
            data=dict(token=token, public=public),
            files=raw_files,
            # cert=cert,
            allow_redirects=True,
            cookies={"from-my": "browser"},
        )

        url = f"{protocol}://{response.text}"

        try:
            pyperclip.copy(url)
            print(
                "[bold green]Success[/bold green]: [bold]copied url[/bold] to clipboard."
            )
        except:
            print("[bold green]Success[/bold green]")
            logging.warning("Could not copy url to clipboard.")
        print(url)


if __name__ == "__main__":
    args = parser.parse_args()
    logging.info(args)
    share_file(
        file=args.file,
        urls=args.urls,
        method=args.method,
        token=args.token,
        cert=args.cert,
        # expiration=args.expiration,
        public=args.public,
    )
