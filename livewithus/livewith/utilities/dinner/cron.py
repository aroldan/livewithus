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

#Actions to be taken with a cron job.
def dinner_cron(current_time=datetime.now()):
	try:
		HMUtility.objects.get(name="Dinner")
	except:
		init_dinner()
	#Houses that need new polls
	active_settings = DinnerHouseSettings.objects.filter(active=True)
	
	for s in active_settings:
		house = s.house
		hour = current_time.hour
		##GENERATE POLL##
		#if the house's time zone is in midnight
		if timezone_adjust(0, house.settings.time_zone)==hour:
			#generate a new dinner poll
			generate_poll(house.pk)
	
		##NOTIFY##
		#if the house's time zone time matches the push notifications time
		if timezone_adjust(DinnerHouseSettings.objects.get(house=house).push_hour, house.settings.time_zone)==hour:	
			try:
				poll = DinnerPoll.objects.filter(house=house).order_by('-timeCreated')[0]
			except: 
				poll = None
			if poll:
				respondants = poll.respondants()
				for person in house.getHouseMembers():
					if person not in respondants:
						dinner_notify(person)

def init_dinner():
	"""initializes dinner into the database"""
	dinner_utility = HMUtility()
	dinner_utility.name = "Dinner"
	dinner_utility.avatar = "img/utilities/dinner_icon.jpg"
	dinner_utility.summary_template = "alpha/utilities/dinner/settings/summary.html"
	dinner_utility.save()
	return dinner_utility

def generate_poll(house_id):
	"""method called to generate a dinner poll for a specific house"""
	dinner_poll = DinnerPoll()
	dinner_poll.house = House.objects.get(id=house_id)
	try:
		dinner_poll.creator = HMUtility.objects.get(name="Dinner")
	except:
		dinner_poll.creator = init_dinner()
	dinner_poll.text = "What are you doing for dinner?"
	dinner_poll.save()
	
	
def dinner_notify(person):

	n = Notification()
	n.person = person
	n.origin = "dinner"
	n.template_path = "/utilities/dinner/dinner_notification.html"
	n.subject = "Please sign in for dinner on livewith.us"
		
	# dispatch notifications
	n.send({'person':person})

#TODO: Use django's built in timezone modules
def timezone_adjust(hour, timezone):
	if timezone == 'EST':
		gmt = hour + 5
	if timezone == 'CST':
		gmt =  hour + 6
	if timezone == 'MST':
		gmt = hour + 7
	if timezone == 'PST':
		gmt = hour + 8
	if gmt > 23:
		gmt = 0
	if gmt < 0:
		gmt = 23
	return gmt
		


	 