#!/usr/bin/env python
# Setup script for livewith.us -- sets up required tables

import os
import sys
sys.path = ['/home/livewith/webapps/django/'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'djsite.settings'
from djsite import settings
from django.core.management import setup_environ

# set up django environment
setup_environ(settings)

from photologue.models import ImageModel, PhotoSize
from livewith.models import *

LIVEWITH_PHOTO_SIZES = { 'thumb' : { 'width': 30,
                                    'height': 30,
                                    'crop': True
                                     },
                          'smthumb' : { 'width': 20,
                                    'height': 20,
                                    'crop': True
                                     },
                          'settingsthumb' : { 'width': 50,
                                    'height': 50,
                                    'crop': True
                                     },
                          'housesidebar' : {
                                    'width': 160,
                                    'height': 160,
                                    'crop': True
                                           }
                        }
# now build 'em

print "Setting up thumbnail sizes..."
for ps, psettings in LIVEWITH_PHOTO_SIZES.iteritems():
    thisps = LIVEWITH_PHOTO_SIZES[ps]
    try:
        t = PhotoSize.objects.get(name=ps)
        print "Image crop size %s already exists, skipping." % ps
    except PhotoSize.DoesNotExist: # create chat_sized_thumbnail
        p = PhotoSize(name=ps,
                      width = psettings['width'],
                      height = psettings['height'],
                      crop = psettings['crop']
                      )
        p.save()

print "Setting up Utility settings..."

print "Setup complete."
