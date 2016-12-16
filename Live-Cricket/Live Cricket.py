import sys
import requests
import time
from PySide import QtCore, QtGui
from bs4 import BeautifulSoup
from time import sleep
I1 = []
I2 = []
Links=[]
MInfo=[]


class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        url = "http://www.espncricinfo.com/ci/engine/match/index.html?view=live"
        r = requests.get(url)
        soup = BeautifulSoup(r.content,"html.parser")
        inng1 = soup.find_all("div",{"class":"innings-info-1"})
        inng2= soup.find_all("div",{"class":"innings-info-2"})
        
        for item in inng1:
                I1.append(item.text.rstrip())
        for item in inng2:
                I2.append(item.text.lstrip())
        for l1,l2 in zip(I1,I2):
            MInfo.append(l1+ " Vs. " +l2)

        data = soup.find_all("div",{"class":"match-articles"})
        for item in data:
                scr1=item.find_all("a")
                Links.append("http://www.espncricinfo.com"+ scr1[0].get("href"))
           
        for item in MInfo:
            action = menu.addAction(item)
            self.setContextMenu(menu)
            action.triggered[()].connect(
            lambda item=item: self.getScore(item))
       
        
    def getScore(self,item):
        
        
        newmenu1 = QtGui.QMenu()
        newmenu2 = QtGui.QMenu()
        icon = QtGui.QIcon("C:\Python34\C.png")
        i=MInfo.index(item)
        url=(Links[i])

        while True:
            II1=[]
            II2=[]
            r = requests.get(url)
            soup = BeautifulSoup(r.content,"html.parser")
        
            team1 = soup.find_all("div",{"class":"team-1-name"})
            team2 = soup.find_all("div",{"class":"team-2-name"})
            TOSS = soup.find_all("div",{"class":"innings-requirement"})
            
            

            urlmain = "http://www.espncricinfo.com/ci/engine/match/index.html?view=live"
            r1 = requests.get(urlmain)
            
            soup1 = BeautifulSoup(r1.content,"html.parser")
            inng1 = soup1.find_all("div",{"class":"innings-info-1"})
            inng2 = soup1.find_all("div",{"class":"innings-info-2"})
            
                
            for item in inng1:
                II1.append(item.text.rstrip())
            for item in inng2:
                II2.append(item.text.lstrip())
            innings1=II1[i].replace(team1[0].text,'')

            if any(word in team1[0].text for word in II1[i]):
                innings1=II1[i].replace(team1[0].text,'')
                print(innings1)
                TEAM1SCORE = team1[0].text.rstrip() + " : " + innings1.lstrip()
                innings2=II2[i].replace(team2[0].text,'')
                if innings2=="":
                    TEAM2SCORE=""
                else:
                    TEAM2SCORE = team2[0].text.rstrip() + " : " + innings2.lstrip()
                
            else:
                innings1=II1[i].replace(team2[0].text,'')
                TEAM1SCORE = team2[0].text + " : " + innings1.lstrip()
                innings2=II2[i].replace(team1[0].text,'')
                if innings2=="":
                    TEAM2SCORE=""
                else:
                    TEAM2SCORE = team1[0].text.rstrip() + " : " + innings2.lstrip()

            self.tray = QtGui.QSystemTrayIcon()
            self.tray.setIcon(icon)
            self.tray.setContextMenu(newmenu1)
            self.tray.show()
            self.tray.showMessage("Live Cricket Score","\n" + TEAM1SCORE + "\n" + TEAM2SCORE + "\n"+ TOSS[0].text.lstrip()  )
            
            sleep(15)

def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("C:\Python34\C.png"), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
