#!/usr/bin/env python
from notifiers import notify
notify('pushover', user='foo', token='bar', message='test')
