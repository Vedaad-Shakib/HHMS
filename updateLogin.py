#!/usr/bin/env python

import urllib
import urllib2
import cookielib

def updateLogin():
    # for some REALLY odd reason, urllib.urlopen(url) returns a fake site (probably PCR precautions)
    # you have to send a request instead
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('LoginUser', 'PCR')]
    urllib2.install_opener(opener)
    url = 'https://webappsca.pcrsoft.com/Clue/Student-Portal-Login-LDAP/8464?returnUrl=https%3a%2f%2fwebappsca.pcrsoft.com%2fClue%2fDefault.aspx%3fpid%3d7536'
    
    # fake so we can just get form
    auth = {
        'user': '<username>',
        'password': '<password>'
        }
    data = urllib.urlencode(auth)
    req = urllib2.Request(url, data)
    loginSite = urllib2.urlopen(req)
    loginContents = loginSite.read().replace("8464", "loginSubmit/")
    
    loginFile = open("templates/login.html", "w")
    loginFile.seek(0)
    loginFile.write(loginContents)
    loginFile.close()
