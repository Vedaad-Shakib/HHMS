from django.shortcuts  import render_to_response
from django.conf       import settings
from django.template   import RequestContext
from django.http       import HttpResponseRedirect
from django.http       import HttpResponse

from apps.settings     import *

import urllib
import urllib2
import cookielib


def home(request):
    return render_to_response( 'login.html',
                               { },
                               context_instance=RequestContext(request))

def loginSubmit(request):
    if not request.POST:
        return HttpResponseRedirect('/')
    else:
        # send POST request with request.POST
        return HttpResponseRedirect('/')
