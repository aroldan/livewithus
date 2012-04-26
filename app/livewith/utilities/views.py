from django.template import Context, loader
from django.template import Template, Context
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from livewith.decorators import house_required
from django.http import HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext
from django.http import Http404 
from django.db.models import Q
from livewith.forms import * 
from django.core.files import File
from datetime import date
from datetime import datetime
import random
import string
import os

from livewith.models import *
from livewith.utilities.models import *
from livewith.utilities.dinner.models import *

from livewith.utilities.dinner.views import define_dinner_house_settings


# Views.py for a utility should only have to contain utility handlers.
# Display is handled in render.py and normal view logic is contained there

def define_utility_settings(house):
	#define dinner settings
	if not DinnerHouseSettings.objects.filter(house):
		define_dinner_house_settings(house)
		
