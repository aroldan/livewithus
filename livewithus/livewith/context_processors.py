from django.contrib.auth.models import User
from livewith.models import House
from livewith.models import Person

def	currenthouse(request):
	"Gets the current house and user-linked person object."
	if(request.user.is_authenticated()):
		try:
			person = request.user.get_profile()
			house = person.GetLastHouse()
			if house:
				# all views should get the current house, the current person, and alerts for that person
				return { 'house' : house, 'person': person, 'alerts' : person.get_alerts(house), 'house_debt': house.house_debt(person.pk)}
			else:
				return { 'person': person }
		except ValueError: # return no house
			return {}
		except Person.DoesNotExist:
			return {}
	else:
		return {}
		