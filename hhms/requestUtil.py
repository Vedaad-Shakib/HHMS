#!/usr/bin/env python                                                                                                                                                                                      
# author Vedaad Shakib

import urllib
import urllib2
import cookielib
import requests
import re

def updateLogin():
    '''# for some REALLY odd reason, urllib.urlopen(url) returns error for PCR (and not for other sites)                            
    # you have to send a request instead                   
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('LoginUser', 'PCR')]
    urllib2.install_opener(opener)
    url = 'https://webappsca.pcrsoft.com/Clue/Student-Portal-Login-LDAP/8464?returnUrl=https%3a%2f%2fwebappsca.pcrsoft.com%2fClue%2fDefault.aspx%3fpid%3d7536'

    # random form just to send request                                     
    auth = {
            'user': '<username>',
            'password': '<password>'
           }
    data = urllib.urlencode(auth)
    req = urllib2.Request(url, data)
    loginSite = urllib2.urlopen(req)
    loginContents = loginSite.read()'''

    url = "https://webappsca.pcrsoft.com/Clue/Student-Portal-Login-LDAP/8464?returnUrl=https%3a%2f%2fwebappsca.pcrsoft.com%2fClue%2fDefault.aspx%3fpid%3d7536"

    r = requests.get(url)
    loginContents = r.text

    # parse
    loginContents = re.sub("action[ ]*=[ ]*['\"].*?['\"]", "action=\"loginSubmit/\"", loginContents, count=1)
    loginContents = loginContents.replace("Student Portal Login LDAP", "HHMS")
    loginContents = loginContents.replace("Student Portal Login (LDAP)", "HHMS")


    # add csrf token                                                                                                                                                                                       
    formTag = re.findall("<form.*?>", loginContents)[0]
    tagIndex = loginContents.index(formTag)
    insertIndex = tagIndex + len(formTag) + 1
    loginContents = loginContents[:insertIndex+1] + "{% csrf_token %}" + loginContents[insertIndex+1:]

    loginFile = open("templates/login.html", "w")
    loginFile.seek(0)
    loginFile.write(loginContents)
    loginFile.close()

 
def sendPostRequest(url, **auth):
    r = requests.post(url, data=auth)
    return r.text
