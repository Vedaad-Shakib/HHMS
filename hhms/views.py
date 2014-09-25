from django.shortcuts  import render_to_response
from django.conf       import settings
from django.template   import RequestContext
from django.http       import HttpResponseRedirect
from django.http       import HttpResponse

from apps.settings     import *
from hhms.requestUtil  import *

import urllib
import urllib2
import cookielib

def log(value):
    file = open("140925.log", "w")
    file.write(str(value))
    file.close()

def home(request):
    return render_to_response( 'login.html',
                               { },
                               context_instance=RequestContext(request))

def loginSubmit(request):
    if not request.POST:
        return HttpResponseRedirect('/')
    else:
        auth = {}
        for key, value in request.POST.iteritems():
            try:
                auth[str(key)] = int(value)
            except:
                auth[str(key)] = str(value)


        url = "https://webappsca.pcrsoft.com/Clue/Student-Assignments/7536"
        pcr = sendPostRequest(url, **auth)

        log(auth)

        return HttpResponseRedirect('/')
