from django.conf.urls.defaults import patterns
from django.views.generic.simple import redirect_to

urlpatterns = patterns(                    
    'livewith.utilities.dinner.views',  
    (r'house_settings_handler$', 'house_settings_handler'),   
    (r'pollhandler$', 'dinner_poll_handler'), 
    (r'deactivate$', 'deactivate'), 
    (r'activate$', 'activate'),           
    (r'$', redirect_to, {'url': '/lw/settings/#utilities'}), # redirect to settings for utilities
    )
