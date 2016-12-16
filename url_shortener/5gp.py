#!/usr/bin/env python

import requests
import sys

site_url = 'http://5.gp/'
# Uncomment the next line for http://qr.net
# site_url = 'http://qr.net/'

def shortener(urls):
    for url in urls:
        response = requests.get(site_url + 'api/short?longurl=%s' %url)
        print eval(response.text)['url']

if __name__ == '__main__':
    shortener(sys.argv[1:])
