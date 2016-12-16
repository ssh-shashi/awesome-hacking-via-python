#!/usr/bin/env python

import requests
import sys

def shortener(**kwargs):
    for values in kwargs.values():
        for value in values:
            short_url = requests.get('http://tinyurl.com/api-create.php?url=%s' %value)
            print short_url.text

if __name__ == '__main__':
    shortener(url=sys.argv[1:])
