from django.db import models
from livewith.models import House, HMCreator, Person
from djsite.polymorphic.models import DowncastMetaclass
import djsite.settings

class HMUtility(HMCreator):
	"Base class for Utilities. All utilities must extend this model."
	
	name = models.CharField(max_length=32)
	avatar = models.ImageField(upload_to="uploads/utilities/", blank = True)
	path = models.CharField(max_length=255, null=True, blank=True) # optional path, to be used in the case of 3rd party utilities hosted off-server
	summary_template = models.CharField(max_length=200)

	def get_avatar(self):
		if self.avatar:
			return '/site_media/%s' % self.avatar
		else:
			return djsite.settings.DEFAULT_AVATAR

	def get_sm_avatar(self):
		if self.avatar:
			return '/site_media/%s' % self.avatar
		else:
			return djsite.settings.DEFAULT_AVATAR

	def __unicode__(self):
		return self.name
	
		
class UtilityHouseSettings(models.Model):
	"""
	Base class defining House-specific settings for Utilities.
	Extensions of this class should define utility settings specific to a house.
	"""
	house = models.ForeignKey(House)
	utility = models.ForeignKey(HMUtility)
	active = models.BooleanField()
	template = models.CharField(max_length=200)
	
	__metaclass__ = DowncastMetaclass
	
class UtilityPersonSettings(models.Model):
	"""
	Base class defining User/Person-specific settings for Utilities.
	Extensions of this class should define utility settings specific to a user.
	"""
	person = models.ForeignKey(Person)
	utility = models.ForeignKey(HMUtility)
	active = models.BooleanField()
	template = models.CharField(max_length=200)
	
	__metaclass__ = DowncastMetaclass
	
	
	