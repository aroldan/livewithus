from django.conf import settings
from django.http import HttpResponseRedirect
from livewith.models import House

def house_required(view, redirect_field_name = settings.HOUSE_NEEDED_URL):
	"""
	Decorator for views that checks that the user logged in has a house and
	if house_id is specified, if a house is specified.
	to the house creation page if necessary.
	"""
	def _check(request, house_id, *args, **kwargs):
		h = House.objects.get(pk=house_id)
		if(request.user.get_profile().isInHouse(h)):
			return view(request, house_id, *args, **kwargs)
		else:
			request.user.message_set.create(message="You do not have permission to view that house.")
			return HttpResponseRedirect("/lw/")
	return _check