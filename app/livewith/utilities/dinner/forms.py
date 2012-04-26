from django import forms
from django.forms import ModelForm
from livewith.utilities.dinner.models import DinnerHouseSettings, DinnerPersonSettings
class DinnerHouseSettingsForm(ModelForm):
	
	class Meta:
		model = DinnerHouseSettings
		
class DinnerPersonSettingsForm(ModelForm):
	
	class Meta:
		model = DinnerPersonSettings