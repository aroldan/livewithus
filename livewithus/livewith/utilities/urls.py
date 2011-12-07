from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.defaults import patterns
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    (r'crontab/', 'run_utility_crons'),
    (r'dinner/', include('livewith.utilities.dinner.urls')),
    (r'$', redirect_to, {'url': '/lw/settings/#utilities'}), # redirect to settings for utilities
)
