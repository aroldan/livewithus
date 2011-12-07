from livewith.models import *
from livewith.utilities.models import *
from livewith.utilities.dinner.models import *
from django.contrib import admin

admin.site.register(HMUtility)
admin.site.register(Person)
admin.site.register(House)
admin.site.register(HMChatter)
admin.site.register(HMCreator)
admin.site.register(HMPoll)
admin.site.register(PollOption)
admin.site.register(Tag)
admin.site.register(Vendor)
admin.site.register(Residency)
admin.site.register(Purchase)
admin.site.register(HMTransaction)
admin.site.register(ApprovalCode)
admin.site.register(Debt)
admin.site.register(UserPreferences)
admin.site.register(HousePreferences)
admin.site.register(Settlement)
admin.site.register(Alert)
admin.site.register(PollResponse)
admin.site.register(PersonAvatar)
admin.site.register(HouseAvatar)


admin.site.register(UtilityHouseSettings)
admin.site.register(UtilityPersonSettings)

admin.site.register(DinnerHouseSettings)
admin.site.register(DinnerPersonSettings)
admin.site.register(DinnerPoll)
admin.site.register(DinnerResponse)