#!/usr/bin/env python

import os
import random
import logging

from notifypy import Notify
from yaml import safe_load


class NotificationMemo(Exception):
    def __str__(self):
        return "NOTIFY_MEMO environment variable must be set to\
    the path of the icon"


memo_path = os.environ.get("NOTIFY_MEMO")
if not memo_path:
    raise NotificationMemo

with open(memo_path, "r") as file:
    memo = safe_load(file)

tips = memo["tips"]
tips = list(tips.items())
tip = random.choice(tips)
logging.info(str(tip))

notification = Notify()

logging.info(f"memo: {memo_path}")
# notify.application_name="Tips",
notification.title = tip[0]
icon_path = os.environ.get("NOTIFY_ICON")
if icon_path:
    logging.info(f"icon: {icon_path}")
    notification.icon = icon_path
audio_path = os.environ.get("NOTIFY_AUDIO")
if audio_path:
    logging.info(f"audio: {audio_path}")
    notification.audio = audio_path
notification.message = tip[1]["message"]
notification.send()
