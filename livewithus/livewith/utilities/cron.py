#!/usr/bin/env python
import os
import sys
import time
from datetime import datetime
sys.path = ['/home/livewith/webapps/django/'] + sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'djsite.settings'
from djsite import settings
from django.core.management import setup_environ

setup_environ(settings)

from livewith.utilities.dinner.cron import dinner_cron

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-t", "--time", action="store", type="string")

(options, args) = parser.parse_args()

def do_crons():
    if options.time:
        datest = time.strftime("%y-%m-%d ")
        current_time = datetime.fromtimestamp(time.mktime(time.strptime(datest + options.time, "%y-%m-%d %H:%M:%S")))
        
        dinner_cron(current_time)
    else:
        dinner_cron()
    
if __name__ == '__main__':
    do_crons()
