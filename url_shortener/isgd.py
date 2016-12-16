#!/usr/bin/env python

import requests
import sys
from re import findall

site_url = 'http://is.gd/'
# Uncomment the next line for http://v.gd
# site_url = 'http://v.gd/'

def shortener(urls):
    for url in urls:
        response = requests.get(site_url + 'create.php?url=%s' %url)
        data = response.headers.get('set-cookie')
        print site_url + str(findall("recent=(.+?);", data)[0])

if __name__ == '__main__':
    shortener(sys.argv[1:])
