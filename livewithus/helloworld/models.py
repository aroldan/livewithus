from django.db import models

# Create your models here.
class UserInfo(models.Model):
	email = models.EmailField()
	signupDate = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return self.email + " on " + str(self.signupDate)