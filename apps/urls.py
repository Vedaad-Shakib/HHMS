from django.conf.urls import url
from django.conf.urls import patterns
from django.conf.urls import include
from django.conf      import settings

from django.contrib    import admin

urlpatterns = patterns('hhms.views',
                       url(r'^$',           'login' ),
                       url(r'^weekly/$',    'weekly'),
                       url(r'^daily/$',     'daily' ),
                       url(r'^faq/$',       'faq'   )
)

urlpatterns += patterns('',
                        (r'^.*/media/(?P<path>.*)$', 'django.views.static.serve',
                                                     {'document_root': settings.MEDIA_ROOT}),
                        (r'media/(?P<path>.*)$',     'django.views.static.serve',
                                                     {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += patterns('',
                        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                        url(r'^admin/', include(admin.site.urls)),
)
