from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import django.views.generic.simple
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^djsite/', include('djsite.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    #helloworld stie URLs
    (r'^$', 'livewith.views.index'),
    (r'^pages/(?P<page_name>\w+)/$', 'livewith.views.pageview'),
    
    (r'^lw/', include('livewith.urls')),
    (r'^analytics/', include('livewith.analytics.urls')),
)

# static content serving -- for local dev only
if settings.DEBUG:
	urlpatterns += patterns('',
	    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'C:/livewithus/site_media', 'show_indexes': True}), 
	)
