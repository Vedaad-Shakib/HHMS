from django.shortcuts  import render_to_response
from django.conf       import settings
from django.template   import RequestContext
from django.http       import HttpResponseRedirect
from django.http       import HttpResponse

from apps.settings     import *
from hhms.requestUtil  import *
from datetime          import date
from datetime          import timedelta
from datetime          import datetime
from time              import time

from StringIO import StringIO
import pycurl

def login(request):
    if not request.POST:
        return render_to_response('login.html',
                                  {},
                                  context_instance=RequestContext(request))

def faq(request):
    return render_to_response('faq.html',
                              {},
                              context_instance=RequestContext(request))

def daily(request):
    # check for post data or set cookie (in the case of switching back and forth between weekly and daily)
    try:
        username = request.POST["username"]
        password = request.POST["password"]
        request.session["username"] = username
        mode = "auth"
    except:
        try:
            currMonth = request.session["schedule"]
            username  = request.session["username"]
            mode = "cookie"
        except:
            return HttpResponseRedirect("/")

    # for viewing previous or future days
    if "timedelta" in request.GET:
        dt = int(request.GET["timedelta"])
    else:
        dt = 0

    if mode == "auth":
        page = getPage(getAuth(str(username), str(password)))

        #strange error that you sometimes have to sent two requests
        if "Student Portal Login" in page or "Object moved to" in page:
            page = getPage(getAuth(str(username), str(password)))

        currMonth = parsePage(page)
        request.session["schedule"] = currMonth

        mode = getMode(page)
        # day mode has too little information
        if mode != "Month" and mode != "Week":
            return render_to_response("login.html",
                                      {"error": True,
                                       "mode":  mode,},
                                      context_instance=RequestContext(request))

    # today's date
    today = date.today() + timedelta(dt)
    if today.weekday() == 5:
        today += timedelta(2)
    if today.weekday() == 6:
        today += timedelta(1)

    # tomorrow's date, excluding weekends
    if today.weekday() < 4:
        tomorrow = today + timedelta(1)
    else:
        tomorrow = today + timedelta(7-today.weekday())

    # parse into correct format
    homework = []
    classes = {}
    nClasses = 0
    for i in currMonth:
        if not classes.has_key(str(i[1])):
            classes[i[1]] = nClasses
            nClasses += 1
            homework.append([i[1], [], [], []])

        if i[3].date() == today:
            homework[classes[str(i[1])]][1].append([i[0], i[4], i[5]])
        elif i[3].date() == tomorrow:
            homework[classes[str(i[1])]][2].append([i[0], i[4], i[5]])
        elif i[2].date() <= today and i[3].date() > tomorrow and i[0] != "Classwork":
            homework[classes[str(i[1])]][3].append([i[0], i[3].strftime("%m/%d/%y"), i[4], i[5]])

    # remove duplicates (sometimes PCR source code has duplicates)
    for i in range(len(homework)):
        for j in range(len(homework[i])):
            if j == 0:
                continue
            if j == len(homework[i])-1:
                homework[i][j].sort(key=lambda x: (x[0], x[1], x[2], x[3]))
            else:
                homework[i][j].sort(key=lambda x: (x[0], x[1], x[2]))
            for k in range(len(homework[i][j])-1, 0, -1):
                if homework[i][j][k] == homework[i][j][k-1]: del(homework[i][j][k])

    dates = [today.strftime("%A, %b %d"), tomorrow.strftime("%A, %b %d"), "Due Later"]
    today = today.strftime("%B %d, %Y")

    return render_to_response("studentPageDaily.html",
                              {"homework": homework,
                               "nClasses": nClasses,
                               "name":     str(username)[2:-1].title(),
                               "dates":    dates,
                               "today":    today,
                               "next":     str(dt+1),
                               "prev":     str(dt-1)},
                              context_instance=RequestContext(request))


def weekly(request):
    # if there is post data or previous cookie data
    try:
        username = request.POST["username"]
        password = request.POST["password"]
        request.session["username"] = username
        mode = "auth"
    except:
        try:
            currMonth = request.session["schedule"]
            username  = request.session["username"]
            # can't store datetime in cookie, so 
            mode = "cookie"
        except:
            return HttpResponseRedirect("/")

    if "timedelta" in request.GET:
        dt = int(request.GET["timedelta"])
    else:
        dt = 0

    #return HttpResponse(getPage(getAuth(str(username), str(password))))

    if mode == "auth":
        page      = getPage(getAuth(str(username), str(password)))
    
        # strange error that you sometimes have to send two requests
        if "Student Portal Login" in page or "Object moved to" in page:
            page  = getPage(getAuth(str(username), str(password)))


        
        # parsing only supports month mode
        mode = getMode(page)
        if mode != "Month" and mode != "Week":
            return render_to_response('login.html',
                                      {"error": True,
                                       "mode":  mode,},
                                      context_instance=RequestContext(request))

        currMonth = parsePage(page)
        request.session["schedule"] = currMonth

    # a timedelta to add to date such that friday, saturday, and sunday display next week's schedule, essentially
    # making it such that the week, as defined by this program, starts on friday at 2:40
    weekDelta = timedelta(2, 33600) # difference between monday 0:00, "start" of week, and friday 2:40, when school starts
    
    today = datetime.today() + weekDelta + timedelta(dt)
    friday = today + timedelta(4-today.weekday())
        
    # 4d list:
    # first dimension: all classes (0th elementh is name of class)
    # second dimension: all days
    # third dimension: assignments for that day for that class
    # fourth dimension: the information contained within that assignment (type, title, description)
    #                   for the due later list, the information contained is (type, date, title, description)
    homework = []
    # maps class name to index in "homework" array
    classes = {}
    nClasses = 0
    for i in currMonth:
        # i: [type, class name, start date, end date, title, description]
        if not classes.has_key(str(i[1])):
            classes[i[1]] = nClasses
            nClasses += 1
            homework.append([i[1], [], [], [], [], [], []])

        # if the assignment is in this week, append it to the respective weekday
        if i[3].isocalendar()[1] == ((today).isocalendar()[1] % 52):
            homework[classes[str(i[1])]][i[3].weekday()+1].append([i[0], i[4], i[5]])
        # if today is after the start date and before the end date, add it to the "Due Later" list
        elif i[2] <= friday and i[3] > friday and i[0] != "Classwork":
            homework[classes[str(i[1])]][6].append([i[0], i[3].strftime("%m/%d/%y"), i[4], i[5]])

    # remove duplicates (sometimes PCR source code has duplicates)
    for i in range(len(homework)):
        for j in range(len(homework[i])):
            if j == 0:
                continue
            else:
                homework[i][j].sort(key=lambda x: (x[0], x[1], x[2]))
            for k in range(len(homework[i][j])-1, 0, -1):
                if homework[i][j][k] == homework[i][j][k-1]: del(homework[i][j][k])

    # get displayed dates
    today = datetime.today() + weekDelta + timedelta(dt)
    dates = [(today - timedelta(days=today.weekday()-i)).strftime("%A, %b %d") for i in range(5)]
    today = (today - timedelta(days=today.weekday())).strftime("%B %d, %Y")
    dates.append("Due Later")

    return render_to_response('studentPageWeekly.html',
                              {"homework": homework,
                               "nClasses": nClasses,
                               "name":     str(username)[2:-1].title(),
                               "dates":    dates,
                               "today":    today,
                               "next":     str(dt+7),
                               "prev":     str(dt-7)},
                              context_instance=RequestContext(request))
    

