from django.conf.urls import url
from django.conf.urls import patterns
from django.conf.urls import include
from django.conf      import settings

urlpatterns = patterns('hhms.views',
                       url(r'^$',           'login' ),
                       url(r'^weekly/$',    'weekly'),
                       url(r'^daily/$',     'daily' ),
)

urlpatterns += patterns('',
                        (r'^.*/media/(?P<path>.*)$',         'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT}
                         ),
                        (r'media/(?P<path>.*)$',             'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT}
                         ),
                        )
