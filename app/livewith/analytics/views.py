from django.template import Context, loader
from django.template import Template, Context
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from livewith.decorators import house_required
from django.http import HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext
from django.http import Http404 
from django.db.models import Q
from livewith.forms import * 
from django.core.files import File
from django.db.models import Sum
from datetime import date
from datetime import datetime
import random
import string
import os

from livewith.models import *
from livewith.utilities.models import *

@staff_member_required 
def dashboard(request):
	today = datetime.now()
	houses = House.objects.all()
	for house in houses:
		house.active_settings = UtilityHouseSettings.objects.filter(house=house).filter(active=True)
		house.chats =  HMChatter.objects.filter(house=house).filter(timeCreated__year=today.year).filter(timeCreated__month=today.month).count()
		house.purchases = HMTransaction.objects.filter(house=house).filter(timeCreated__year=today.year).filter(timeCreated__month=today.month).count()
		sum = Debt.objects.filter(transaction__house=house).filter(transaction__timeCreated__year=today.year).filter(transaction__timeCreated__month=today.month).aggregate(sum=Sum('value'))
		house.dollars = sum['sum']
		house.totalchats =  HMChatter.objects.filter(house=house).count()
		house.totalpurchases = HMTransaction.objects.filter(house=house).count()
		sum = Debt.objects.filter(transaction__house=house).aggregate(sum=Sum('value'))
		house.totaldollars = sum['sum']
	return render_to_response("alpha/analytics/dashboard.html", {'houses':houses})

@staff_member_required 
def house_view(request, house_id):
	house = House.objects.get(id=house_id)
	house.active_settings = UtilityHouseSettings.objects.filter(house=house).filter(active=True)
	return render_to_response("alpha/analytics/overview.html", {'house':house})


@staff_member_required 
def chatter(request, house_id):
	house = House.objects.get(id=house_id)
	chats = HMChatter.objects.filter(house=house)
	return render_to_response("alpha/analytics/chatter.html", {'house':house, 'chats':chats})
		
@staff_member_required 
def finances(request, house_id):
	house = House.objects.get(id=house_id)
	purchases = HMTransaction.objects.filter(house=house)
	return render_to_response("alpha/analytics/finances.html", {'house':house, 'purchases':purchases})
		

@staff_member_required
def push_alerts(request):
	return render_to_response("alpha/analytics/push_alerts.html")

@staff_member_required
def do_push(request):
	persons = Person.objects.all()
	for person in persons:
		alert = Alert()
		alert.person = person
		alert.house = person.GetLastHouse()
		alert.related_objects = {'text':request.POST['text']}
		alert.template_path = "system_alert.html"
		alert.save()
	return redirect("/analytics/")


