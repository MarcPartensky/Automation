#!/usr/bin/env python

"""
Send markdown file to the website of Marc Partensky
as an article to be read by others.
"""

import os
import argparse
import requests
import logging
import yaml

# from rich import print

CONFIG_PATH = os.path.abspath(
    os.path.join(os.environ["PROGRAMS_PATH"], "automation", "markdown.yml")
)

with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)


if not config:
    logging.info("Config file path not found. Falling back to default config.")
    config = dict(url=[os.environ["WEBSITE_URL"]])

logging.info(f"config: {config}")

parser = argparse.ArgumentParser(
    description=__doc__,
)

parser.add_argument("file", help="file to send")

parser.add_argument(
    "-u", "--url", dest="urls", nargs="+", default=config["url"], help="website url"
)

parser.add_argument(
    "-m", "--method", nargs="?", default=config["method"], help="http method"
)

parser.add_argument("-v", "--vars", nargs="+", help="http variables (post/get/...)")

parser.add_argument(
    "-c", "--config", default=config, help="Change default config file."
)


def send_markdown(
    file: str, urls: list = [], method: str = "POST", vars: list = [], config: dict = {}
):
    """Send a markdown file to the website."""
    path = file.replace("./", "")
    file = path.split("/")[-1]

    with open(path, "r") as f:
        content = f.readlines()

    # check for empty file
    content = "\n".join(content[1:]).strip()
    if content == "":
        raise Exception("This file is empty!")

    raw_files = {"file": (file, content)}

    for url in urls:
        url = url.replace("http://", "").replace("https://", "")
        logging.info(f"Sending file to {url}.")

        # response = session.request(method=method, url=url, params=vars, files=raw_files)

        try:
            response = requests.post(
                f"https://{url}/api/upload-markdown/", files=raw_files, data=args.vars
            )
        except:
            logging.warning(f"No https for {url}, falling back to http.")
            response = requests.post(
                f"http://{url}/api/upload-markdown/", files=raw_files, data=args.vars
            )

        if response.status_code != 200:
            logging.error(response)
        else:
            print(f"{url}/article/{file.replace('.md', '')}")


if __name__ == "__main__":
    args = parser.parse_args()
    logging.info(args)
    send_markdown(args.file, args.urls, args.method, args.vars, args.config)
