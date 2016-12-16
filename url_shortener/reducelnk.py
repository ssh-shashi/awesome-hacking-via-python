#!/usr/bin/env python

import requests
import sys

def shortener(urls):
    for url in urls:
        response = requests.get('http://reducelnk.com/api.php?task=quicken&url=%s&ad=2' %url)
        print eval(response.text)['link'].replace('\/', '/')

if __name__ == '__main__':
    shortener(sys.argv[1:])
