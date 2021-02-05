#!/usr/bin/env python
"""
Send markdown file to the website of Marc Partensky
as an article to be read by others.
"""

import os
import sys
import requests
import argparse
import yaml

parser = argparse.ArgumentParser(
    description=__doc__,
)

parser.add_argument(
    '--url', '-u',
    type='str',
    default=os.environ['WEBSITE_URL'],
    help="website url"
)

parser.add_argument(
    '--method', '-m',
    type='str',
    default='POST',
    help="http method"
)

args = parser.parse_args()


# BASE_URL = os.environ['WEBSITE_URL']

path = sys.argv[1].replace('./', '')
file = path.split('/')[-1]

with open(path, 'r') as f:
    content = f.readlines()

content = '\n'.join(content[1:]).strip()
if content == '':
    raise Exception("This file is empty!")

url = f"{args['url']}/api/upload-markdown/"

raw_files = {'file': (file, content)}

response = requests.post(url, files=raw_files)
if response.status_code != 200:
    print(response)
else:
    print(f"{args['url']}/article/{file.replace('.md', '')}")
