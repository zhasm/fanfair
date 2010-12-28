from django.conf.urls.defaults import *
from view import *
import os
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
STATIC_DOC_ROOT = os.path.join(os.path.dirname(__file__), 'media').replace('\\','/')
urlpatterns = patterns('',
    # Example:
    # (r'^fanfair/', include('fanfair.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r"^$", index),
    (r"^who$", who),
    (r"^login$", login),
    (r'^site_media/(?P<path>.*/?)$', 'django.views.static.serve',
            {'document_root': STATIC_DOC_ROOT}),
    
)
