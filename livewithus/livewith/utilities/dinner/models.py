from livewith.utilities.models import *
from livewith.models import CONTACT_METHODS, DEFAULT_CONTACT_METHOD, HMAction
from django.db import models
from livewith.utilities.dinner import render
from livewith.models import *

DINNER_CHOICES = (
	('E', 'Eating'),
	('C', 'Cooking'),
	('S', 'Skipping'),
)	

class DinnerHouseSettings(UtilityHouseSettings):
	push_hour = models.PositiveIntegerField()
	push_minute = models.PositiveIntegerField()
	
	def get_house_settings_template(self):
		return self.template
	
	
class DinnerPersonSettings(UtilityPersonSettings):
	notification_method = models.CharField(choices=CONTACT_METHODS, max_length=1, default=DEFAULT_CONTACT_METHOD)

class DinnerPoll(HMChatter):
	
	def delete_responses(self, person):
		responses = DinnerResponse.objects.filter(person = person, dinner_poll = self)
		responses.delete()

	def respondants(self):
		respondants = []
		
		responses = DinnerResponse.objects.filter(dinner_poll = self)
		for response in responses:
			respondants.append(response.person)
		return respondants

	def get_eaters(self):
		eaters = []
		es = DinnerResponse.objects.filter(response='E', dinner_poll=self)
		for e in es:
			eaters.append(e.person.pk)
		return eaters
	
	def get_cookers(self):
		cookers = []
		cs = DinnerResponse.objects.filter(response='C', dinner_poll=self)
		for c in cs:
			cookers.append(c.person.pk)
		return cookers
	
	def get_skippers(self):
		skippers = []
		ss = DinnerResponse.objects.filter(response='S', dinner_poll=self)
		for s in ss:
			skippers.append(s.person.pk)
		return skippers

	def get_template_url(self):
		return "alpha/utilities/dinner/dinner_poll.html"

	def __unicode__(self):
		return self.text


class DinnerResponse(HMAction):
	response =  models.CharField(choices=DINNER_CHOICES, max_length=140)
	dinner_poll = models.ForeignKey(DinnerPoll, related_name='response_set')
	
	def __unicode__(self):
		return "%s is %s on %s" % (self.person.user.username, self.response, self.dinner_poll.timeCreated)
	

