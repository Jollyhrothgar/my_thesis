#!/usr/bin/env python

from os import listdir
from os.path import isfile, join
from os.path import expandvars
import re

mypath = expandvars("$VERNIERSIMCONFIG")

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

process_list = []
for f in onlyfiles:
    matches = re.search('\d{6}_step_(\d{2}).conf',f)
    if matches:
        number = matches.group(1)
        if int(number) == 00:
            print number
            process_list.append("%s/%s"%(mypath,f))

for l in process_list:
    print l
