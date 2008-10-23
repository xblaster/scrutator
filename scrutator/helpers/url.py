"""
url.py

Created by X-Blaster on 2008-10-23.
Copyright (c) 2008 lo2k.net.
"""

import re

def detect_link(message):
    p = re.compile('(http://|www\.)[^ ]*', re.IGNORECASE)
    m = p.search(message)
    
    if not m:
        return m
    
    else:
        return m.group()

def get_comment(message):
    separator = ['<=','=>','<-','->','<','>']
    for sep in separator:
        if sep in message:
            comm, comm2 = message.split(sep,1)
            if not 'http' in comm2:
                return comm2.strip()
            return comm.strip()
    return ''