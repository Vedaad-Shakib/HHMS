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

def login(request):
    start = time()
    if not request.POST:
        return render_to_response('login.html',
                                  {},
                                  context_instance=RequestContext(request))

def weekly(request):
    # if there is post data
    try:
        username = request.POST["username"]
        password = request.POST["password"]
    except:
        return HttpResponseRedirect("/")
    
    page      = getPage(str(username), str(password))
    
    # strange error that you sometimes have to send two requests
    if "Student Portal Login" in page:
        page  = getPage(str(username), str(password))
        
    currMonth = parsePage(page)

    # parsing only supports month mode
    mode = getMode(page).lower()
    if mode != "month":
        return render_to_response('login.html',
                                  {"error": True,
                                   "mode": mode,},
                                  context_instance=RequestContext(request))

    # a timedelta to add to date such that friday, saturday, and sunday display next week's schedule
    weekDelta = timedelta(2, 33600) # difference between monday 0:00, "start" of week, and friday 2:40, when school starts
    # parse 
    homework = []
    classes = {}
    nClasses = 0
    for i in currMonth:
        if classes.has_key(str(i[1])):
            if i[3].isocalendar()[1] == ((datetime.today()+weekDelta).isocalendar()[1] % 52):
                homework[classes[str(i[1])]][i[3].weekday()+1].append([i[0], i[4], i[5]]) 
            elif i[2] <= datetime.today() and i[3] > datetime.today()+timedelta(1) and i[0] != "Classwork":
                homework[classes[str(i[1])]][6].append([i[0], i[3].strftime("%m/%d/%y"), i[4], i[5]])
        else:
            classes[i[1]] = nClasses
            nClasses += 1
            homework.append([i[1], [], [], [], [], [], []])
            if i[3].isocalendar()[1] == ((datetime.today()+weekDelta).isocalendar()[1] % 52):
                homework[classes[str(i[1])]][i[3].weekday()+1].append([i[0], i[4], i[5]]) 
            elif i[2] <= datetime.today() and i[3] > datetime.today()+timedelta(1) and i[0] != "Classwork":
                homework[classes[str(i[1])]][6].append([i[0], i[3].strftime("%m/%d/%y"), i[4], i[5]])

    # remove duplicates (sometimes PCR source code has duplicates)
    for i in range(len(homework)):
        homework[i][-1].sort(key=lambda x: (x[0], x[1], x[2], x[3]))
        for j in range(len(homework[i][-1])-1, 0, -1):
            if homework[i][-1][j] == homework[i][-1][j-1]: del(homework[i][-1][j])

    # get displayed dates
    today = datetime.today()
    dates = [(today - timedelta(days=today.weekday()-i)).strftime("%A, %b %d") for i in range(5)]
    today = (today-timedelta(days=today.weekday())).strftime("%B %d, %Y")
    dates.append("Due Later")

    return render_to_response('studentPageWeekly.html',
                              {"homework": homework,
                               "nClasses": nClasses,
                               "name":     str(username)[2:-1].title(),
                               "dates":    dates,
                               "today":    today},
                              context_instance=RequestContext(request))
        
        
 
