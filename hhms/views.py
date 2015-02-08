from django.shortcuts  import render_to_response
from django.conf       import settings
from django.template   import RequestContext
from django.http       import HttpResponseRedirect
from django.http       import HttpResponse

from apps.settings     import *
from hhms.requestUtil  import *
from datetime          import date

def login(request):
    if not request.POST:
        return render_to_response('login.html',
                                  {},
                                  context_instance=RequestContext(request))
    else:
        username = request.POST["username"]
        password = request.POST["password"]

        page      = getPage(str(username), str(password))
        
        # strange error that you sometimes have to send two requests
        if "Login" in page:
            page  = getPage(str(username), str(password))
            
        currMonth = parsePage(page)

        mode = getMode(page)
        if mode != "Month":
            return render_to_response('login.html',
                                      {"error": True,
                                       "mode": mode,},
                                      context_instance=RequestContext(request))

        homework = []
        classes = {}
        nClasses = 0
        for i in currMonth:
            if classes.has_key(str(i[1])):
                if i[3].isocalendar()[1] == date.today().isocalendar()[1] and i[3].day > 1:
                    homework[classes[str(i[1])]][i[3].day-1].append((i[0], i[4], i[5])) 
            else:
                classes[i[1]] = nClasses
                nClasses += 1
                homework.append([i[1], [],[],[],[], [], []])
                if i[3].isocalendar()[1] == date.today().isocalendar()[1] and i[3].day > 1:
                    homework[classes[str(i[1])]][i[3].day-1].append((i[0], i[4], i[5])) 

        classes = sorted(classes, key=classes.get)

        return render_to_response('studentPageWeekly.html',
                                  {"homework": homework,
                                   "nClasses": nClasses,
                                   "classes":  classes,
                                   "name":     str(username)[2:-1].title() + " " + str(username)[-1].title() + "."},
                                  context_instance=RequestContext(request))
    
