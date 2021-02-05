#!/usr/bin/env python
import launchd

for job in launchd.jobs():
    print(job.label, job.pid, job.laststatus, job.properties, job.plistfilename)
