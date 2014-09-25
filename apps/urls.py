from django.conf.urls import url
from django.conf.urls import patterns
from django.conf.urls import include

urlpatterns = patterns('hhms.views',
    url(r'^$',             'home'       ),
    url(r'^loginSubmit/$', 'loginSubmit'),
)
