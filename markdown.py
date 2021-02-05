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
    os.path.join(
        os.environ['PROGRAMS_PATH'],
        'automation',
        'markdown.yml'
    )
)

with open(CONFIG_PATH, 'r') as file:
    config = yaml.safe_load(file)

logging.info(config)

parser = argparse.ArgumentParser(
    description=__doc__,
)

parser.add_argument(
    'file',
    help="file to send"
)

parser.add_argument(
    '-u', '--url',
    nargs='+',
    default=config['url'],
    help="website url"
)

parser.add_argument(
    '-m', '--method',
    nargs='?',
    default=config['method'],
    help="http method"
)

parser.add_argument(
    '-v', '--vars',
    nargs='+',
    help="http variables (post/get/...)"
)

args = parser.parse_args()
logging.info(args)

# BASE_URL = os.environ['WEBSITE_URL']

path = args.file.replace('./', '')
file = path.split('/')[-1]

with open(path, 'r') as f:
    content = f.readlines()

content = '\n'.join(content[1:]).strip()
if content == '':
    raise Exception("This file is empty!")

raw_files = {'file': (file, content)}

for url in args.url:
    url = url.replace('http://', '').replace('https://', '')
    logging.info(f"Sending file to {url}.")

    try:
        response = requests.post(
            f"https://{url}/api/upload-markdown/",
            files=raw_files
        )
    except:
        logging.warning(
            f"No https for {url}, falling back to http.")
        response = requests.post(
            f"http://{url}/api/upload-markdown/",
            files=raw_files
        )

    if response.status_code != 200:
        logging.error(response)
    else:
        print(f"{url}/article/{file.replace('.md', '')}")
