#!/usr/bin/python

from StringIO import StringIO
from bs4      import BeautifulSoup
from datetime import date
from datetime import datetime
import pycurl
import re
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def getSession():
    header = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, "https://webappsca.pcrsoft.com/Clue/Student-Assignments/7536")
    c.setopt(c.HEADERFUNCTION, header.write)
    c.perform()
    c.close()
    
    return re.findall("Set-Cookie: ASP\.NET_SessionId=.*?;", header.getvalue())[0][30:-1]

def getAuth(username, password):
    c = pycurl.Curl()
    c.setopt(c.COOKIE, "ASP.NET_SessionId=kvjstdjnxg5eryjobhrj1mc2; pcrSchool=Harker; WebSiteApplication=97")
    c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, "ctl00_ctl00_RadScriptManager1_TSM=%3B%3BAjaxControlToolkit%2C+Version%3D4.1.40412.0%2C+Culture%3Dneutral%2C+PublicKeyToken%3D28f01b0e84b6d53e%3Aen-US%3Aacfc7575-cdee-46af-964f-5d85d9cdcf92%3Aea597d4b%3Ab25378d2&ctl00_ctl00_RadStyleSheetManager1_TSSM=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=VXmilAnuSBQ8jvaobUklnuxLtBjVUq3C0NvY1%2B0l9QV5x4e2nDcsiJwAJ%2F%2B2o2TLzvL%2FTJmlegx6XKoxCTF24kCwsFqFseXeKihX93EyKAEfGIcUiIDpnuzQqT%2F5UDe3zs6bCoinmikqRdbjCaaoSSmoyV2EpkxiDQb2TXTpO2DKO57D892%2F%2BJrcu7Ut%2FnZwu2IvIlINwmgMQuBNVtyaqBDK9oO2CA76puED%2FyMdCzU2kPBWCmYNbmf5M%2BTT%2BDOH%2FHSves%2BmecvV8qsFcB2glHwx3%2FgKuxJkLFjpCJ48bvY9bPZeYC1Uyv97YHSQsJxVTAedhz2Xi0arMFgAwe4rR74eDAd9yW%2FrbedNCB%2BoBK1cTqHmmzCC8jEr4m2eD%2BRi7sUkLfFg1zS6nbx%2F4eDJ4kDlyd8QktE1Am05sauRhogTt2A33IE8%2FGTKI4vPFGGRy0hVFqzLK8%2FCeXIjpWd1n2NxO1d4FNoA0T3MvFYIq4AnvrVtQ5DYMLegg%2FYSsIC3vhbjzoYQk32BIKCTb%2FKwA4lJ3hWlw8taLe7gSZ%2BKaqAtW66rtpn48ZFdjsnNm6heJunOaPS4rts4uPuRp%2F%2F5UesfRGuQdQRu2AMPxf6Ex3MZgLBfbEuLsdfkMmcRVSK03JVoh9rt%2F5lHYMwp6v%2FilwcsbU%2B4bfhSmM66%2BSbmU4lp6hgoAz8QHloiHM1LS%2FGjb55GkJtkKNU7rK7ADCFu3xqr547M07zsDYTS479u63axQayt0%2Fyf3BmWeE2UpGEKkT%2BlbU0AwMPGTdlCkF%2BHlQNbc5tkNw%2BI%2FD45dQnmXYeKQIc2Q1nUAVmCrjTaKk2ZTuhQKWRLfMuCd3%2BpSJoh%2BsVRhEOnihPvZZpZJ3fdWF7l3kTF9ixIOJgXxjEi1p97em1pkfhyHW1%2BDfSzijX4uyeQtjZtSqZ34IU6vfDvd7m8Tgjk6oFIRBCZV7YWWjAbl9o2qg9ku%2BO8jeHwqeRXO84OsS0X%2Bim2%2FOmz%2BLVTTtO4zhIGHrnzNsOcIs6jVkGNCR89pPJ6iktkfA2TqvZPiLPuPz2yKHzXToPJJC%2BhRxaVqPMGx5HOq5slcHn8yeRyEFza0jqGYX96IXjUF%2FwG0QVdKxOMg0CBju6NL%2F7%2BvRAlBY0p15tPPbvBdG9yO0Hhed3LgxmKbM6mCp9CMsSujcxpeTaE2KvxnBF25Ji5g2Lr8udKquOrRSeijzj4sMPNbOQxhT%2FFDj%2F%2B6dwvvhQDk1oZSeFhDax3C0lf9tc7lObAlQ1W1cT7Pt3jp3%2BH0KKTld51IXnZZniUzrQ704N7QrnMChdXqPwRLXXR3GYB3%2Frv1B6HpdUINSBWKKYsUa7mtMWGt5%2BvI5nzvPAMI08qOgvwZo0tktfIw8qqbi7eR3kVL4SqKj9lP4m%2F2Xl0bKiH3h7iEhX8PKq%2BDVoFeqfr5UbMFoI7ArvKV41bQrD4zGokCdWH811UAlBMx1bdUpY4aPITfyQWrwK1gqB1Ad3QHVa6DTNRKmRbqIIjtHiMCXicH4Je76heq0FKu4nR%2Fvn5wnXee%2FlljsJ0XuP9DApggqnB7af79Prn5eP2gkLa0RdbtplO8QNPq2sitrSW1cugNNEPpwf8UEv%2Fbf7gZC56uC9GSxr5zIBaCKGwTZJSQjN3f3MYSAAn%2Fp47PZ1eOw3x7a92D6SvSnybUigT655GXjSLr0s%3D&__VIEWSTATEGENERATOR=94F9FD60&ctl00_ctl00_RadFormDecorator1_ClientState=&ctl00%24ctl00%24baseContent%24panelFullCover%24hfId=&ctl00%24ctl00%24baseContent%24headerContainer%24hfId=&ctl00%24ctl00%24baseContent%24logoLink%24hfId=&ctl00%24ctl00%24baseContent%24logoLink%24hfCssClass=&ctl00%24ctl00%24baseContent%24SingleNavigationMenuNavUtil%24hfId=&ctl00%24ctl00%24baseContent%24SingleNavigationMenuNavUtil%24hfCssClass=&ctl00%24ctl00%24baseContent%24SingleNavigationMenuWeb%24hfId=&ctl00%24ctl00%24baseContent%24SingleNavigationMenuWeb%24hfCssClass=&ctl00%24ctl00%24baseContent%24SingleNavigationMenuNavConst%24hfId=&ctl00%24ctl00%24baseContent%24SingleNavigationMenuNavConst%24hfCssClass=&ctl00%24ctl00%24baseContent%24SiteMapPath1%24hfId=&ctl00%24ctl00%24baseContent%24baseContent%24flashTop%24ctl00%24Login1%24UserName="+username+"&ctl00%24ctl00%24baseContent%24baseContent%24flashTop%24ctl00%24Login1%24Password="+password+"&ctl00%24ctl00%24baseContent%24baseContent%24flashTop%24ctl00%24Login1%24RememberMe=on&ctl00%24ctl00%24baseContent%24baseContent%24flashTop%24ctl00%24Login1%24LoginButton=Log+In&ctl00%24ctl00%24baseContent%24baseContent%24flashTop%24ctl00%24hfId=49894&ctl00%24ctl00%24baseContent%24baseContent%24flashTop%24hfId=45326&ctl00%24ctl00%24baseContent%24baseContent%24secondary%24hfId=&ctl00%24ctl00%24baseContent%24baseContent%24mainPlaceHolder%24hfId=&ctl00%24ctl00%24baseContent%24baseContent%24mainCenter%24hfId=&ctl00%24ctl00%24baseContent%24baseContent%24mainBottom%24hfId=&ctl00%24ctl00%24baseContent%24baseContent%24rightContent%24hfId=&ctl00%24ctl00%24baseContent%24baseContent%24rightContentCenter%24hfId=&ctl00%24ctl00%24baseContent%24baseContent%24insideFooter%24hfId=&ctl00%24ctl00%24baseContent%24WebFooter%24hfId=")
    source = StringIO()
    header = StringIO()
    c.setopt(c.WRITEFUNCTION, source.write)
    c.setopt(c.HEADERFUNCTION, header.write)
    c.setopt(c.URL, "https://webappsca.pcrsoft.com/Clue/Student-Portal-Login-LDAP/8464")
    c.perform()
    c.close()

    return re.findall("Set-Cookie: \.ASPXAUTH=.*?;", header.getvalue())[0][22:-1]

def getPage(auth):
    source = StringIO()
    c = pycurl.Curl()
    c.setopt(c.COOKIE, ".ASPXAUTH="+auth+"; ASP.NET_SessionId="+getSession()+"; pcrSchool=Harker; WebSiteApplication=97")
    c.setopt(c.URL, "https://webappsca.pcrsoft.com/Clue/Student-Assignments/7536")
    postFields = open("hhms/monthPost.txt", "r").read()
    c.setopt(c.POSTFIELDS, postFields) # invariably get the month
    c.setopt(c.WRITEFUNCTION, source.write)
    c.perform()
    c.close()

    return source.getvalue()

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
        body  = [j.strip() for j in i.find_all(class_="rsAptContent")[0].find_all("div")[3].getText().split("\n") if j.strip()]
        dates = [map(int, j.split("/")) for j in re.findall("\d+/\d+/\d+", body[0])]

        tmp.append(i["title"][:nameStart])
        tmp.append(i["title"][nameStart+2:nameEnd])
        tmp.append(datetime(dates[0][2], dates[0][0], dates[0][1]))
        try: tmp.append(datetime(dates[1][2], dates[1][0], dates[1][1]))
        except: tmp.append(datetime(dates[0][2], dates[0][0], dates[0][1]))
        tmp.append(i["title"][nameEnd+13:])
        try: tmp.append(body[2])
        except: tmp.append("") # no description
        
        homework.append(tmp)
    return homework
