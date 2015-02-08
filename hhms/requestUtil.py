#!/usr/bin/python

from StringIO import StringIO
from bs4      import BeautifulSoup
from datetime import date
import pycurl
import re
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def getPage(username, password):
    storage = StringIO()
    c=pycurl.Curl()
    c.setopt(c.URL, "http://webappsca.pcrsoft.com/Clue/Default.aspx?pid=8464")
    c.setopt(c.COOKIE, "ASP.NET_SessionId=lsfhrhalgzfcaev5kr11b1ut; pcrSchool=Harker; WebSiteApplication=97")
    c.setopt(c.COOKIEJAR, "/Users/farzin/cookie.txt")
    c.setopt(c.POST, 1)
    # the post fields that the login page contains
    c.setopt(c.POSTFIELDS, 'ctl00_ctl00_RadScriptManager1_TSM=&ctl00_ctl00_RadStyleSheetManager1_TSSM=&__EVENTTARGET=ctl00$ctl00$baseContent$baseContent$flashTop$ctl00$RadScheduler1&__EVENTARGUMENT={"Command":"SwitchToMonthView"}&__VIEWSTATE=/wEPDwUENTM4MQ9kFgJmD2QWAmYPZBYEAgEPZBYEAgMPFgIeBGhyZWYFMS8vd3d3Lmhhcmtlci5vcmcvdXBsb2FkZWQvdGhlbWVzL3Bjci9oYXJrZXItMi5jc3NkAggPFgIfAGRkAgMPZBYEZg9kFgQCBQ8PFggeFUVuYWJsZUVtYmVkZGVkU2NyaXB0c2ceHEVuYWJsZUVtYmVkZGVkQmFzZVN0eWxlc2hlZXRnHhJSZXNvbHZlZFJlbmRlck1vZGULKXNUZWxlcmlrLldlYi5VSS5SZW5kZXJNb2RlLCBUZWxlcmlrLldlYi5VSSwgVmVyc2lvbj0yMDE0LjMuMTIwOS40NSwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj0xMjFmYWU3ODE2NWJhM2Q0AR4XRW5hYmxlQWpheFNraW5SZW5kZXJpbmdoFgIeBXN0eWxlBQ1kaXNwbGF5Om5vbmU7ZAIJD2QWAgIBD2QWCAIBD2QWAgICD2QWAgIBDxYEHg9TdG9yZWRQb3NpdGlvbnMFAnt9Hg1TdG9yZWRJbmRpY2VzBQJ7fWQCAw9kFgICAg9kFgICAQ8WBB8GBQJ7fR8HBQJ7fWQCDw9kFhACAQ9kFgRmDw8WBB4IQ3NzQ2xhc3NlHgRfIVNCAgJkFgICAQ9kFgICAQ88KwAKAQAPFgIeEkRlc3RpbmF0aW9uUGFnZVVybAU7aHR0cHM6Ly93ZWJhcHBzY2EucGNyc29mdC5jb20vQ2x1ZS9TdHVkZW50LUFzc2lnbm1lbnRzLzc1MzZkFgJmD2QWAgIPDxAPFgIeB0NoZWNrZWRnZGRkZAICDxYCHgVDbGFzc2UWAgIBDxYEHwYFAnt9HwcFAnt9ZAIDD2QWAgICD2QWAgIBDxYEHwYFAnt9HwcFAnt9ZAIFD2QWAgICD2QWAgIBDxYEHwYFAnt9HwcFAnt9ZAIHD2QWAgICD2QWAgIBDxYEHwYFAnt9HwcFAnt9ZAIJD2QWAgICD2QWAgIBDxYEHwYFAnt9HwcFAnt9ZAILD2QWAgICD2QWAgIBDxYEHwYFAnt9HwcFAnt9ZAIND2QWAgICD2QWAgIBDxYEHwYFAnt9HwcFAnt9ZAIPD2QWAgICD2QWAgIBDxYEHwYFAnt9HwcFAnt9ZAIRD2QWAgICD2QWAgIBDxYEHwYFAnt9HwcFAnt9ZAIBD2QWAgIBD2QWAgICD2QWAgIBDxYEHwYFAnt9HwcFAnt9ZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBAUdY3RsMDAkY3RsMDAkUmFkRm9ybURlY29yYXRvcjEFRGN0bDAwJGN0bDAwJGJhc2VDb250ZW50JGJhc2VDb250ZW50JGZsYXNoVG9wJGN0bDAwJExvZ2luMSRSZW1lbWJlck1lBTljdGwwMCRjdGwwMCRiYXNlQ29udGVudCRMb2dvdXRDb250cm9sMSRMb2dpblN0YXR1czEkY3RsMDEFOWN0bDAwJGN0bDAwJGJhc2VDb250ZW50JExvZ291dENvbnRyb2wxJExvZ2luU3RhdHVzMSRjdGwwMzoUthGamq/qv5BsNvGsB2HduUDV&__VIEWSTATEGENERATOR=94F9FD60&ctl00_ctl00_RadFormDecorator1_ClientState=&ctl00$ctl00$baseContent$panelFullCover$hfId=&ctl00$ctl00$baseContent$headerContainer$hfId=&ctl00$ctl00$baseContent$logoLink$hfId=&ctl00$ctl00$baseContent$logoLink$hfCssClass=&ctl00$ctl00$baseContent$SingleNavigationMenuNavUtil$hfId=&ctl00$ctl00$baseContent$SingleNavigationMenuNavUtil$hfCssClass=&ctl00$ctl00$baseContent$SingleNavigationMenuWeb$hfId=&ctl00$ctl00$baseContent$SingleNavigationMenuWeb$hfCssClass=&ctl00$ctl00$baseContent$SingleNavigationMenuNavConst$hfId=&ctl00$ctl00$baseContent$SingleNavigationMenuNavConst$hfCssClass=&ctl00$ctl00$baseContent$SiteMapPath1$hfId=&ctl00$ctl00$baseContent$baseContent$flashTop$ctl00$Login1$UserName='+username+'&ctl00$ctl00$baseContent$baseContent$flashTop$ctl00$Login1$Password='+password+'&ctl00$ctl00$baseContent$baseContent$flashTop$ctl00$Login1$RememberMe=&ctl00$ctl00$baseContent$baseContent$flashTop$ctl00$Login1$LoginButton=Log In&ctl00$ctl00$baseContent$baseContent$flashTop$ctl00$hfId=49894&ctl00$ctl00$baseContent$baseContent$flashTop$hfId=45326&ctl00$ctl00$baseContent$baseContent$secondary$hfId=&ctl00$ctl00$baseContent$baseContent$mainPlaceHolder$hfId=&ctl00$ctl00$baseContent$baseContent$mainCenter$hfId=&ctl00$ctl00$baseContent$baseContent$mainBottom$hfId=&ctl00$ctl00$baseContent$baseContent$rightContent$hfId=&ctl00$ctl00$baseContent$baseContent$rightContentCenter$hfId=&ctl00$ctl00$baseContent$baseContent$insideFooter$hfId=&ctl00$ctl00$baseContent$WebFooter$hfId=')
    c.setopt(c.FOLLOWLOCATION, 1)
    c.setopt(c.SSL_VERIFYPEER, 0)
    c.setopt(c.HEADER, 1)
    c.setopt(c.WRITEFUNCTION, storage.write)
    c.perform()
    c.close()

    return storage.getvalue()

def getMode(text):
    soup = BeautifulSoup(text)
    return str(soup.find_all(class_="rsSelected")[0].getText())

def parsePage(text):
    soup = BeautifulSoup(text)
    content = soup.find_all(class_="rsContentTable")[0]
    homework = []
    # parses content
    # contains type, class name, start date, end date, assignment title, assignment details
    for i in content.find_all(class_="rsAptSimple"):
        tmp = []
        nameEnd = max(max(max(i["title"].find("MTRF"), i["title"].find("MWRF")), i["title"].find("MTWF")), i["title"].find("MTWR"))-7
        nameStart = i["title"].find("\r")
        body = [j.strip() for j in i.find_all(class_="rsAptContent")[0].find_all("div")[2].getText().split("\n")]
        dates = [map(int, j.split("/")) for j in re.findall("\d+/\d+/\d+", body[3])]

        tmp.append(i["title"][:nameStart])
        tmp.append(i["title"][nameStart+2:nameEnd])
        tmp.append(date(dates[0][2], dates[0][0], dates[0][1]))
        try: tmp.append(date(dates[1][2], dates[1][0], dates[1][1]))
        except: tmp.append(date(dates[0][2], dates[0][0], dates[0][1]))
        tmp.append(i["title"][nameEnd+13:])
        tmp.append(body[10])
        
        homework.append(tmp)
    return homework
