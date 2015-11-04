from StringIO  import StringIO
from bs4       import BeautifulSoup
from datetime  import date
from datetime  import datetime
import pycurl
import re
import time
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))

def getSession():
    header = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, "https://webappsca.pcrsoft.com/Clue/Student-Assignments/7536")
    c.setopt(c.HEADERFUNCTION, header.write)
    c.perform()
    c.close()
    
    return re.findall("Set-Cookie: ASP\.NET_SessionId=.*?;", header.getvalue())[0][30:-1]

def getAuth(username, password):
    header = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, "https://webappsca.pcrsoft.com/Clue/Student-Portal-Login-LDAP/8464?returnUrl=https%3a%2f%2fwebappsca.pcrsoft.com%2fClue%2fStudent-Assignments-End-Date-(No-Range)%2f18593")
    c.setopt(c.POST, 1)
    a = os.getcwd()
    c.setopt(c.POSTFIELDS, open(os.path.join(BASE, "authPost.txt")).read().replace("<USERNAME>", username).replace("<PASSWORD>", password))
    c.setopt(c.HTTPHEADER, [i.strip() for i in open(os.path.join(BASE, "authHeaders.txt"))])
    c.setopt(c.HEADERFUNCTION, header.write)

    c.perform()
    c.close()

    return re.findall("Set-Cookie: \.ASPXAUTH=.*?;", header.getvalue())[0][22:-1]

def getPage(auth):
    source = StringIO()
    c = pycurl.Curl()
    c.setopt(c.COOKIE, ".ASPXAUTH="+auth+"; ASP.NET_SessionId="+getSession()+"; pcrSchool=Harker; WebSiteApplication=97")
    '''
    c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, open(os.path.join(BASE, "authPostNext.txt"), "r").read())
    '''
    #c.setopt(c.COOKIEJAR, "cookie.txt")
    #c.setopt(c.COOKIEFILE, "cookie.txt")
    
    c.setopt(c.FOLLOWLOCATION, 1)
    c.setopt(c.URL, "https://webappsca.pcrsoft.com/Clue/Student-Assignments/7536")
    c.setopt(c.WRITEFUNCTION, source.write)

    c.setopt(c.COOKIEJAR, 'cookie.txt')
    c.setopt(c.COOKIEFILE, 'cookie.txt');
    c.setopt(c.COOKIEJAR, 'cookie.txt');
    
    
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(c.SSL_VERIFYHOST, False)
    c.perform()
    c.close()

    return source.getvalue()

def getMode(text):
    soup = BeautifulSoup(text)
    return str(soup.find_all(class_="rsSelected")[0].getText())

def getSoup(text):
    soup = BeautifulSoup(text)
    return soup.prettify()

def parsePage(text):
    soup = BeautifulSoup(text)
    content = soup.find_all(class_="rsContentTable")[0]
    homework = []
    # parses content
    # contains type, class name, start date, end date, assignment title, assignment details, links
    for k in range(len(content.find_all(class_="rsAptSimple"))):
        i = content.find_all(class_="rsAptSimple")[k]
        tmp = []
        nameEnd = max(max(max(i["title"].find("MTRF"), i["title"].find("MWRF")), i["title"].find("MTWF")), i["title"].find("MTWR"))-7
        nameStart = i["title"].find("\r")
        body  = [j.strip() for j in i.find_all(class_="rsAptContent")[0].find_all("div")[4].getText().split("\n") if j.strip()]
        if body == []:
            body  = [j.strip() for j in i.find_all(class_="rsAptContent")[0].find_all("div")[5].getText().split("\n") if j.strip()] # PCR's a piece of shit; I have no explanation for why this works
            switch = True # if this seemingly random phenomenon occurs, we have to adjust the other lines as well
        else:
            switch = False
            
        dates = [map(int, j.split("/")) for j in re.findall("\d+/\d+/\d+", body[0])]

        tmp.append(i["title"][:nameStart])
        tmp.append(i["title"][nameStart+2:nameEnd])
        tmp.append(datetime(dates[0][2], dates[0][0], dates[0][1]))
        try: tmp.append(datetime(dates[1][2], dates[1][0], dates[1][1]))
        except: tmp.append(datetime(dates[0][2], dates[0][0], dates[0][1]))
        tmp.append(i["title"][nameEnd+13:])

        if getMode(text) == "Week":
            desc = "".join(map(str, list(i.find_all(class_="rsAptContent")[0].find_all("div")[4+switch].find_all("div")[0].children)[8:])).strip() # get raw description
            desc = re.sub("(<br>|</br>|</p>)*$", "", desc).strip() # strip <br> and whitespace and <p> from ends
            desc = re.sub("^(<p class=.*?>|<br>|</br>)*", "", desc).strip()
            desc = desc.replace("href=\"..", "href=\"https://webappsca.pcrsoft.com/Clue") # fix relative links
        if getMode(text) == "Month":
            desc = "".join(map(str, list(i.find_all(class_="rsAptContent")[0].find_all("div")[4+switch].children)[8:])).strip() # get raw description
            desc = re.sub("(<br>|</br>|</p>)*$", "", desc).strip() # strip <br> and whitespace and <p> from ends
            desc = re.sub("^(<p class=.*?>|<br>|</br>)*", "", desc).strip()
            desc = desc.replace("href=\"..", "href=\"https://webappsca.pcrsoft.com/Clue") # fix relative links

        tmp.append(desc)

        #links = {j.getText(): j["href"].replace("..", "https://webappsca.pcrsoft.com/Clue") for j in i.find_all("a")} # get all links

        #for i in links.keys(): tmp[-1] = tmp[-1].replace(i, "<a href=\""+links[i]+"\">"+i+"</a>") # replace links
        
        homework.append(tmp)
    return homework
