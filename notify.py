#!/usr/bin/env python

from notifypy import Notify
import os

http_path = os.path.abspath("http.svg")
print(http_path)

notification = Notify(
    default_notification_title="title",
    default_application_name="name",
    default_notification_icon=http_path,
    # default_notification_audio=""
)


notification.message = "je te notifie"
notification.send()
