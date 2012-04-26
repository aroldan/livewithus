from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.defaults import patterns
from django.views.generic.simple import redirect_to

urlpatterns = patterns(
    'livewith.analytics.views',
    (r'push_alerts/$', 'push_alerts'),
    (r'do_push/$', 'do_push'),
    (r'(?P<house_id>\w+)/chatter/$', 'chatter'),
    (r'(?P<house_id>\w+)/finances/$', 'finances'),
    (r'(?P<house_id>\w+)/$', 'house_view'),

    (r'$', 'dashboard'),
)
