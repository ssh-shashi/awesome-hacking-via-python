#!/usr/bin/env python

import sys
# Later when complexity will arise we will use option parser
# import argparse
from BeautifulSoup import BeautifulSoup
import requests

htmlclient = {
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5"
}
urilist = []
scorecards = []
espnurl = "http://www.espncricinfo.com"
voice = {
    "0":"Seems you are good @English. Use the index number.",
    "1":"Network Error. Try again later.",
    "2":""
}

def prompt():
    '''
    Returns response from the user
    '''
    try:
        return int(raw_input("Select series: "))
    except ValueError:
        print voice["0"]
        scrapresults(prompt())

def prompt1():
    '''
    Returns response from the user
    '''
    try:
        return int(raw_input("Enter the Scorecard index to view full scorecard: "))
    except ValueError:
        print voice["0"]
        scrap_scorecard(prompt1())

def scrapresults(choice):
    try:
        global htmlclient, urilist, espnurl, scorecards
        url = espnurl + urilist[choice-1].replace("content/current/", "engine/")
        response = requests.get(url, headers=htmlclient)

        # Scraping Results page for the selected series
        if response.status_code==200:
            soup = BeautifulSoup(response.text)
            print soup.title.text + "\n"

            # More work it to be done in this loop as fetch scorecards, man of the match
            for matchestable in soup.findAll("div", attrs={"class":"div630Pad"}):
                scores = [ score.text for score in matchestable.findAll("p", attrs={"class":"potMatchText mat_scores"}) ]
                statuses = [ status.text for status in matchestable.findAll("p", attrs={"class":"potMatchText mat_status"}) ]
                matches = [ matches.text for matches in matchestable.findAll("p", attrs={"class":"potMatchHeading"}) ]
                scorecards = [ tempo.a.get("href") for tempo in matchestable.findAll("span", attrs={"class":"potMatchLink"})]
                
            for num, (score, status, match) in enumerate(zip(scores, statuses, matches)):
                if not score:
                    continue
                else:
                    print match
                    print score
                    print status
                    print "Scorecard index: ", num+1, "\n"
            return
        else:
            print voice["1"]
    except IndexError:
        print "Use the index number left side. Try again."
        scrapresults(prompt())
    except TypeError:
        # Too many function call creating this.
        # 
        #Traceback (most recent call last):
        #  File "cricinfo.py", line 113, in <module>
        #    main()
        #  File "cricinfo.py", line 108, in main
        #    scrapresults(prompt())
        #  File "cricinfo.py", line 29, in prompt
        #   scrapresults(prompt())
        # File "cricinfo.py", line 29, in prompt
        #  scrapresults(prompt())
        #  File "cricinfo.py", line 48, in scrapresults
        #   url = espnurl + urilist[choice-1].replace("content/current/", "engine/")
        #TypeError: unsupported operand type(s) for -: 'NoneType' and 'int'
        pass

def scrap_scorecard(choice):
    try:
        global scorecards
        url = espnurl + scorecards[choice-1]

        print url
    except IndexError:
        print "Use Scorecard index. Try again."
        scrap_scorecard(prompt1())
    except TypeError:
        # Same as above
        pass

def main():
    global htmlclient, urilist, espnurl
    url = espnurl + "/ci/engine/match/scores/live.html"
    response = requests.get(url, headers=htmlclient)
    
    # Scraping Live matches page and getting the info for current international series as a list
    if response.status_code==200:
        soup = BeautifulSoup(response.text)
        for mainNav in soup.findAll("div", attrs={"id":"mainNav"}):
            for table in mainNav.findAll("table", attrs={"width":"270", "border":"0", "cellspacing":"0", "cellpadding":"0"}):
                urilist = [ uri.get("href") for uri in table.findAll("a") ]
    else:
        print voice["1"]

    # Removing unnecessary 'ci' entry from list
    del urilist[-1]

    # View the series to user for selection
    for num, url in enumerate(urilist):
        print num+1, url.split("/")[1]

    scrapresults(prompt())
    scrap_scorecard(prompt1())

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)
# http://www.espncricinfo.com/ci/engine/match/654033.html