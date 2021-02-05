#!/usr/bin/env python
import pync
import os

# pync.notify('Hello World')
# pync.notify('Hello World', title='Python')
# pync.notify('Hello World', group=os.getpid())
# pync.notify('Hello World', activate='com.apple.Safari')
# pync.notify('Github', open='http://github.com/marcpartensky')
pync.notify('test', sound="default", app_icon="http.png")
# pync.notify('test', appIcon="http.png", execute='say "OMG"')

# pync.remove_notifications(os.getpid())

# pync.list_notifications(os.getpid())
