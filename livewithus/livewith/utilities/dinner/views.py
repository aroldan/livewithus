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


# Views.py for a utility should only have to contain utility handlers.
# Display is handled in render.py and normal view logic is contained there

def index(request):
	return render_to_response("test")


@login_required
def dinner_poll_handler(request):
	"""Handle a vote for dinner"""
	person = request.user.get_profile()
	house = House.objects.get(pk=request.POST['house_id'])
	if request.method == 'POST':
		poll_id = int(request.POST['poll_id'])
		poll = DinnerPoll.objects.get(id=poll_id)
		poll.delete_responses(person)
		response = DinnerResponse()
		response.person = person
		response.response = request.POST['poll_'+str(poll_id)+'_for_'+str(person.pk)]
		response.dinner_poll = poll
		response.save()
		
		return redirect('%s' % house.get_absolute_url())
	else:
		return redirect('%s' % house.get_absolute_url())

@login_required	
def activate(request):
	house = House.objects.get(id=request.POST['house_id'])
	dinner = HMUtility.objects.get(name="Dinner")
	settings = DinnerHouseSettings.objects.filter(utility=dinner).filter(house=house)
	if settings:
		settings = settings[0]
		settings.active= True
		settings.save()
	else:
		settings = init_settings(house)
		settings.active=True
		settings.save()
	return redirect('%ssettings/' % house.get_absolute_url())

@login_required	
def deactivate(request):
	house = House.objects.get(id=request.POST['house_id'])
	dinner = HMUtility.objects.get(name="Dinner")
	try:
		settings = DinnerHouseSettings.objects.filter(utility=dinner).filter(house=house)[0]
		settings.active= False
		settings.save()
	except:
		settings = init_settings(house)
		settings.active=False
		settings.save()
	return redirect('%ssettings/' % house.get_absolute_url())

def init_settings(house):
	dinner = HMUtility.objects.get(name="Dinner")
	settings = DinnerHouseSettings()
	settings.utility = dinner
	settings.house = house
	settings.active=False
	settings.push_hour = 12
	settings.push_minute = 00
	settings.template = "alpha/utilities/dinner/settings/house_settings.html"
	settings.save()
	return settings

def house_settings_handler(request):
	house = House.objects.get(id=request.POST['house_id'])
	dinner = HMUtility.objects.get(name="Dinner")
	try:
		settings = DinnerHouseSettings.objects.filter(utility=dinner).filter(house=house)[0]
		settings.push_hour= request.POST['push_hour']
		settings.save()
	except:
		settings = define_house_settings(house)
		settings.push_hour= request.POST['push_hour']
		settings.save()
	return redirect('%ssettings/' % house.get_absolute_url())	
	


