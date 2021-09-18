#!/usr/bin/env python

import os
import random
import logging

from notifypy import Notify

from yaml import safe_load


class NotificationMemo(Exception):
    def __str__(self):
        return "NOTIY_MEMO environment variable must be set to\
    the path of the icon"

class NotificationIcon(Exception):
    def __str__(self):
        return "NOTIY_ICON environment variable must be set to\
    the path of the icon"


print(os.environ.get("NOTIFY"))

memo_path = os.environ.get("NOTIY_ICON")
if not memo_path:
    raise NotificationMemo

image_path = os.environ.get("NOTIY_ICON")
if not image_path:
    raise NotificationNoIcon

with open(memo_path, "r") as file:
    tips = safe_load(file)

tip = random.choice(tips)
print(tip)

logging.info("http_path: " + http_path)

notification = Notify(
    default_notification_title="title",
    default_application_name="name",
    default_notification_icon=http_path,
    # default_notification_audio=""
)
notification.message = "tip"
notification.send()
