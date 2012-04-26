from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.template.defaultfilters import register
from django.db.models import Q
from django.db.models.query import QuerySet
from polymorphic.models import DowncastMetaclass
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from photologue.models import ImageModel
import settings

import decimal
from livewith.fields import PickledObjectField

DEFAULT_CONTACT_METHOD = 'E'

CONTACT_METHODS = (
    ('N', 'Never'),                   
    ('T', 'Text'),
    ('E', 'E-Mail'),
    ('B', 'Text and Email')
)    

CELL_PROVIDERS = (
    ('O', 'None/Other'),
    ('A', 'AT&T'),
    ('N', 'Nextel'),
    ('S', 'Sprint PCS'),
    ('T', 'T-Mobile'),
    ('V', 'Verizon'),
    ('I', 'Virgin Mobile')
                  )
        
class UserPreferences(models.Model):
    """
    Stores preferences for a Pesrson object.
    Abstracted out of Person so it can be adjusted more easily.
    """
    
    #TODO: Include "how often would you like to be contacted"?
    
    updateMethod = models.CharField(max_length=1, choices=CONTACT_METHODS, default="E", verbose_name="How should we contact you?")
    cell_provider = models.CharField(max_length=1, choices=CELL_PROVIDERS, default="O", verbose_name="Cell phone provider?")
    phoneNumber = models.CharField(max_length=10, blank=True, verbose_name="Mobile number (no dashes, spaces)")
    
    def __unicode__(self):
        return "Preferences" #% self.pk

class HousePreferences(models.Model):
    """
    Stores preferences for a House
    """
    
    TIME_ZONES = ( 
                  ('EST', 'Eastern Time'),
                  ('CST', 'Central Time'),
                  ('MST', 'Mountain Time'),
                  ('PST', 'Pacific Time'),
                  ) 

    time_zone = models.CharField(max_length=3, choices=TIME_ZONES, default="EST")
    
    def __unicode__(self):
        return "%s's Preferences" %  self.house.name

class HMCreator(models.Model):
    """
    Base creator class, subclassed by Person and Utility.
    Postings are attributed to an HMCreator; this way they can be attributed
    to actual members of a house (Person) or to automated programs (Utilities)
    """
    
    __metaclass__ = DowncastMetaclass
    
class Person(HMCreator):
    "The user"
    user = models.ForeignKey(User, unique=True)
    cell_phone = models.TextField(max_length = 10, blank = True) #is there a better way to do cell phones?
    settings = models.OneToOneField('UserPreferences')
    
    def get_alerts(self, house):
        "Gets all alerts for this user/house pair, as well as any with no house"
        
        # retrieve alerts ordered by creation time
        alerts = Alert.objects.filter(person=self, acknowledged=False).filter(Q(house=house)|Q(house=None)).order_by('-time')
        return alerts

    def get_avatar(self):
        "Returns the avatar that should be displayed for this person, in thumbnail (30x30) size"
        try:
            self.avatar
        except PersonAvatar.DoesNotExist:
            return djsite.settings.DEFAULT_AVATAR
        
        return self.avatar._get_SIZE_url('thumb')
        
    def get_sm_avatar(self):
        "Returns the avatar that should be displayed for this person, in small thumbnail (20x20) size"
        try:
            self.avatar
        except PersonAvatar.DoesNotExist:
            return djsite.settings.DEFAULT_AVATAR
        
        return self.avatar._get_SIZE_url('smthumb')
    
    def save(self, *args, **kwargs):
        "Custom save method - ensures settings are created"
        try:
            self.settings
        except UserPreferences.DoesNotExist:
            s = UserPreferences()
            s.save() #create user prefs if not defined
            self.settings = s
            
        #now call actual save method.. AVERY    
        super(Person, self).save(*args, **kwargs)

    def numHouses(self):
        residencies = Residency.objects.filter(person=self)
        return residencies.count()

    def isInHouse(self, house):
        "Used in @houserequired decorator. Checks if a user is in a specified house."
        res = Residency.objects.filter(person=self, house=house)
        if res.count() > 0:
            return True
        else:
            return False
    
    @register.filter
    def hasDebt(self, purchase_id):
        "Does this person have the debt?"
        purchase = Purchase.objects.get(id=purchase_id)
        match = Debt.objects.filter(person=self, transaction=purchase)
        if match.count() > 0:
            return match[0].amount()
        else:
            return False

    def GetHouses(self):
        "Gets all the houses that the user belongs to"
        residencies = Residency.objects.filter(person=self)
        #TODO- is there a way to pull houses in one step?
        house_set = []
        for residency in residencies:
            house = House.objects.get(id=residency.house.pk)
            house_set.append(house)
        return house_set
    
    def GetLastHouse(self):
        "Gets the last house the user was logged into"
        residencies = Residency.objects.filter(person=self).order_by('last_login')
        try:
            return residencies[0].house # return first house
        except: # if no house returned, return None
            return None

    def displayName(self):
        "Returns the name to be displayed in the UI"
        if(self.user.get_full_name()):
            return self.user.get_full_name()
        else:
            return self.user.username 
    
    def get_transactions(self, house):
        """
        Returns all transactions related to this Person in a given House.
    
        This set of transactions includes both transactions purchased by this person
        or where the user is in debt.
        
        TODO: include settlements
        """
        transactions = HMTransaction.objects.filter(pk__in=Debt.objects.filter(Q(person=self)|Q(transaction__creator=self)).values_list('transaction_id'))
        return transactions
       
    def get_house_debt(self, house):
        "Returns your total debt or loan related to this Person in a given House"
        total=0
        debts = Debt.objects.filter(person=self, transaction__in = HMTransaction.objects.filter(Q(house= house))) 
        purchases = HMTransaction.objects.filter(creator=self, house=house)
        for debt in debts:
            total = total - debt.value
        for purchase in purchases:
            total = total + decimal.Decimal(purchase.amount())
        return total
    
    def upload_avatar(self, extension, avatar_file):
        "Handle an uploaded avatar."
        
        # delete existing avatar
        try:
            if self.avatar:
                self.avatar.delete()
        except PersonAvatar.DoesNotExist:
            pass #that's fine
            
        #create new avatar
        pa = PersonAvatar(person=self)
        pa.image.save("p_%d_avatar.%s" % (self.pk, extension.lower()), avatar_file)
        pa.save()
        
    def __unicode__(self):
        return self.user.username

class PersonAvatar(ImageModel):
    person = models.OneToOneField(Person, related_name="avatar", primary_key=True)
    
    def __unicode__(self):
        return "Avatar for %s" % self.person.displayName()               

class Tag(models.Model):
    "House wide tracker that can be attached to any HMObject"
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    
class Vendor(models.Model):
    "Third party to whom purchases are attributed"
    name = models.CharField(max_length=50)
    tags = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return self.name

    
class House(models.Model):
    "Group of users"
    name = models.CharField(max_length=50)
    people = models.ManyToManyField('Person',through='Residency') #active users in a house, linked through Residency
    vendor_list = models.ManyToManyField('Vendor', blank=True)
    tag_list = models.ManyToManyField('Tag', blank=True)
    settings = models.OneToOneField('HousePreferences')
    
    def add_to_house(self, member):
        "Add member to this house."
        res = Residency(person=member, house=self, start_date=date.today(), end_date=date.max)
        res.save()
        
        # now send alerts
        self.send_alerts_for_new_member(member)
    
    def send_alerts_for_new_member(self, newUser):
        "Alert all users in this house that a new user joined."
        if newUser.isInHouse(self):
            membersToAlert = self.getHouseMembers()
            for m in membersToAlert: # create alerts to all other users in the house
                if m != newUser:
                    rel_obj = {"new_person_name":newUser.displayName()}
                    a = Alert(person=m, house=self, template_path="new_person_alert.html", related_objects=rel_obj)
                    a.save()
    
    def getHouseMembers(self):
        "Gets all the active members the house has"
        residencies = Residency.objects.filter(house=self)
        #TODO- is there a way to pull houses in one step?
        person_set = []
        for residency in residencies:
            person = Person.objects.get(id=residency.person.pk)
            person_set.append(person)
        return person_set
    
    def save(self,*args, **kwargs):
        "Custom save method - ensures settings are created"
        try:
            self.settings
        except HousePreferences.DoesNotExist:
            s = HousePreferences()
            s.save() #create user prefs if not defined
            self.settings = s
        
        #now call actual save method    
        super(House, self).save(*args, **kwargs) 
        def __unicode__(self):
            return self.name
    def house_debt(self, person_id):
        person = Person.objects.get(id=person_id)
        color=['#736F6E', '#5F5A59', '#504A4B', '#382D2C', '#2B1B17', '#000000','#000000','#000000','#000000','#000000','#000000','#000000','#000000','#000000','#000000','#000000','#000000','#000000','#000000','#000000','#000000']
        debts=[]
        i = 0
        for member in self.getHouseMembers():
            if member.get_house_debt(self)<0:
                if member == person:
                    debts.append({'name':member.displayName(), 'color':'#C11B17', 'pos':0, 'neg':member.get_house_debt(self)})
                else:
                    debts.append({'name':member.displayName(), 'color':color[i], 'pos':0, 'neg':member.get_house_debt(self)})
            else:
                if member == person:
                    debts.append({'name':member.displayName(), 'color':'#347235', 'pos':member.get_house_debt(self), 'neg':0})
                else:
                    debts.append({'name':member.displayName(), 'color':color[i], 'pos':member.get_house_debt(self), 'neg':0})
            i += 1
        
    
        return debts
    
    def get_absolute_url(self):
        return "/lw/%i/" % self.id
    
    def __unicode__(self):
        return self.name
    
    def upload_avatar(self, extension, avatar_file):
        "Handle an uploaded avatar."
        
        # delete existing avatar
        try:
            if self.avatar:
                self.avatar.delete()
        except HouseAvatar.DoesNotExist:
            pass #that's fine
            
        #create new avatar
        ha = HouseAvatar(house=self)
        ha.image.save("h_%d_avatar.%s" % (self.pk, extension.lower()), avatar_file)
        ha.save()

class HouseAvatar(ImageModel):
    house = models.OneToOneField(House, related_name="avatar", primary_key=True)
    
    def __unicode__(self):
        return "Avatar for %s" % self.house.name
    
class ApprovalCode(models.Model):
    "Outgoing approval code to invite people to the site"
    house = models.ForeignKey('House') # house invited to
    person = models.ForeignKey('Person') # person invited from
    email = models.EmailField() # email address originally sent to
    targetPerson = models.ForeignKey(User, null=True, blank=True) # user that was invited, if they already exist
    inviteString = models.CharField(max_length=10, blank=True) #optional invite field, 10 chars
    create_date = models.DateField(auto_now_add=True) # date approval code was created
    
    def get_sender_name(self):
        "Get the name of the person that sent this approval code"
        return self.person.displayName()
    
    def dispatch_email(self):
        """
        Send an email to the person this approval code is targeted at.
        """
        #TODO: Replace with Notification implementation
        
        subject, from_email, to = '%s has invited you to join livewith.us' % self.person.displayName(), 'Livewith.us <info@livewith.us>', self.email

        # build email from template
        html_content = render_to_string('alpha/emails/invite_house_member.html', {'ac':self})
        text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
        
        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
    def dispatch_reminder_email(self):
        "Send a reminder email for this approval code."
        pass

    
    def __unicode__(self):
        return "Invitation to %s code %s" % (self.house.name, self.inviteString)

class Residency(models.Model):
    "Link between a House and a Person"
    person = models.ForeignKey('Person', related_name="person_set")
    house = models.ForeignKey('House')
    start_date = models.DateField(blank=True)
    end_date = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True) # updated every time a user logs into a house
    approvalCode = models.ForeignKey('ApprovalCode', null=True, blank=True) # optional approval code, if the person was invited
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # rent amount last paid
    
    def __unicode__(self):
            return self.person.user.email + " in " + self.house.name
    
class HMAction(models.Model):
    "Action performed by a person. Always abstracted"
    person = models.ForeignKey(Person)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        
class HMObject(models.Model):
    """
    Generic "housemate object"
    """
    creator = models.ForeignKey('HMCreator')
    house = models.ForeignKey(House, blank=True, null=True)
    sticky = models.BooleanField()
    timeCreated = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, blank=True)
    timeModified = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
    
class HMChatter(HMObject):
    "One post (e.g. 'anyone going to the tasting later?')"
    __metaclass__ = DowncastMetaclass # should automatically downcast itself when pulled out of the DB
    
    parent = models.ForeignKey('self', null=True, related_name='child_set', blank=True)
    transaction_parent = models.ForeignKey('HMTransaction', null=True, blank=True, related_name='transaction_child_set')
    text = models.TextField()
    publicly_editable = models.BooleanField()
    
    def get_avatar(self):
        "Returns the avatar that should be displayed for this chat."
        c2 = self.creator.downcast()
        return c2.get_avatar()

    def __unicode__(self):
        return self.text
    
    def notify(self):
        "Notify all involved participants that this Chatter has been created"
        
        for p in self.house.getHouseMembers():
            if p == self.creator.downcast(): # do not notify self
                continue
            n = Notification()
            n.person = p
            n.origin = "chatter"
            n.template_path = "chatter_notification.html"
            if self.parent:
                n.subject = 'Someone added to the conversation: "%s"' % self.parent.text[0:15]
            else:
                n.subject = 'Someone added to the conversation: "%s"' % self.text[0:15]
               
            # dispatch notifications
            n.send({'text' : self.text, 'creator':self.creator.downcast()})
    
class HMPoll(HMChatter):
    "general poll"
    
    def set_text(self, tField):
        option_lines = tField.split("\r\n")
        self.text = option_lines[0]
        
    def get_template_url(self):
        return "alpha/chatter/base_poll.html"
    
    def create_options_from_text(self, tField):
        option_lines = tField.split("\r\n")
        
        # now build the option lines
        for l in option_lines[1:]:
            if l.strip() != "": # ignore blank lines
                o = PollOption()
                o.option_text = l.strip() # strip whitespace
                o.poll = self
                o.creator = self.creator
                o.save()
                
    def option_set_with_people(self):
        option_list = []
        options = PollOption.objects.filter(poll = self)
        for option in options:
            list = []
            responses = PollResponse.objects.filter(vote=option)
            for response in responses:
                list.append(response.person)
            option.list = list
            option_list.append(option)
        
        return option_list
    
    def delete_responses(self, person):
        options = PollOption.objects.filter(poll=self)
        for option in options:
            responses = PollResponse.objects.filter(vote=option, person=person)
            responses.delete()
            
    def notify(self):
        "Notify all involved participants that this Poll has been created"
        
        for p in self.house.getHouseMembers():
            if p == self.creator.downcast(): # do not notify self
                continue
            n = Notification()
            n.person = p
            n.origin = "poll"
            n.template_path = "poll_notification.html"
            if self.parent:
                n.subject = 'Someone added to the poll: "%s"' % self.parent.text[0:15]
            else:
                n.subject = 'Someone added to the poll: "%s"' % self.text[0:15]
                
            # dispatch notifications
            n.send({'house': self.house, 'text' : self.text, 'creator':self.creator.downcast()})

    def __unicode__(self):
        return self.text
        
class PollOption(models.Model):
    "Option one can vote for in a poll"
    creator = models.ForeignKey('HMCreator')
    time = models.DateTimeField(auto_now_add=True)
    
    poll = models.ForeignKey('HMPoll', related_name='option_set')
    option_text = models.CharField(max_length=140)

    def __unicode__(self):
        return ("Poll %s option %s") % (self.poll.text, self.option_text)
    
class SingleVotePoll(HMPoll):
    "Normal poll, one vote per user"
    
    def __unicode__(self):
        return self.text

    
class ExcellencePoll(HMPoll):
    "Excellence voting poll, unlimited votes per user"
    
    def __unicode__(self):
        return self.text 
    
class PollResponse(HMAction):
    "Vote on a poll"
    vote = models.ForeignKey(PollOption)

    def __unicode__(self):
        # Person voted for Option
        return "%s voted for %s " % (self.person.user.username, self.vote.option_text)


class HMTransaction(HMObject):
    "Some kind of financial transaction"
    __metaclass__ = DowncastMetaclass # should automatically downcast itself when pulled out of the DB
    
    purchase_date = models.DateTimeField()
    description = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True) # parent of a transaction for possible historical storage later
    active = models.BooleanField(default=True) # has this been "deleted"?
    
    def amount(self):
        "Return a currency-formatted string with the amount of a transaction."
        debts = Debt.objects.filter(transaction = self)
        amount = 0
        for debt in debts:
            amount += debt.value
        return "%01.2f" % amount
    
    def get_debt(self, person):
        "Gets the debt associated with the person object specified. Returns None if no person."
        try:
            d = Debt.objects.filter(transaction = self, person=person)
            return d[0]
        except:
            return None
        
    def get_all_debts(self):
        "Gets all of the debts associated with the specified transaction"
        try:
            debts = Debt.objects.filter(transaction=self)
            return debts
        except:
            return None
    
    def __unicode__(self):
        return "Purchase by %s on %s" % (self.creator.downcast().user.username, self.purchase_date.isoformat())

class Debt(HMAction):
    "Debt incurred"
    transaction = models.ForeignKey('HMTransaction')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    
    def amount(self):
        "Returns a properly formatted string with this debt's amount"
        return "%01.2f" % self.value
    #guest = models.IntegerField()    #How will the guest feature work?

    def __unicode__(self):
        return "%s was bought, %s owes %s" % (self.transaction.description, self.person.user.username, self.value)


class Purchase(HMTransaction):
    "Expense to a third party Vendor"
    vendor = models.ForeignKey('Vendor')
    
    def get_debts(self):
        return Debt.objects.filter(transaction=self)
    
    def get_creator(self):
        "Gets a creator of a purchase, and downclasses it."
        return self.creator.downcast()
    
    def get_creator_avatar(self):
        c = self.get_creator()
        av = c.get_avatar()
        return av
    
    def __unicode__(self):
        return "%s was bought from %s" % (self.description, self.vendor)
    
class Settlement(HMTransaction):
    "Transfer between Persons in the House"
    banker = models.ForeignKey('Person')
    
    def get_creator(self):
        "Gets a creator of a purchase, and downclasses it."
        return self.creator.downcast()
    
    def get_creator_avatar(self):
        c = self.get_creator()
        av = c.get_avatar()
        return av
    
    def __unicode__(self):
        return "%s was settled from %s" % (self.description, self.banker.user.username)
    
class Alert(models.Model):
    """
    An alert that is sent to a user. It must be acknowledged.
    
    Used in the case of money requests or that sort of thing.
    """
    parent_alert = models.ForeignKey('self', related_name='child_alerts', null=True, blank=True)
    
    person = models.ForeignKey('Person') # person this is for
    house = models.ForeignKey('House', null=True, blank=True) # house this is for
    template_path = models.CharField(max_length=100, default='test_alert.html') # path to a template which tells how to render this Alert
    related_objects = PickledObjectField() # related objects field - pickled object with data for the template
    time = models.DateTimeField(auto_now_add=True) # time created
    acknowledged = models.BooleanField(default=False) # has this Alert been acknowledged?
    
    def __unicode__(self):
        return "Alert %d for %s" % (self.pk, self.person.displayName())
    
    def get_template_url(self):
        return "alpha/alerts/%s" % self.template_path
    
    def acknowledge(self):
        "Called when this is acknowledged. Can set proper clear/archive behavior based on pickled object"
        self.acknowledged = True
        self.save()
        
class Notification(models.Model):
    """
    A notification that is pushed to a user.
    
    The pushing is done using the send() method and is pushed based on user
    preferences and (later) possibly the origin of the notification.
    """
    
    #TODO: How do we want to handle email subjects?
    person = models.ForeignKey(Person, blank=True)
    email = models.EmailField(blank=True)
    origin = models.CharField(max_length=16) #what generated this Notification?
    template_path = models.CharField(max_length=100, default='test_notification.html') # path to a template in templates/alpha/notifications for emails
    template_short_path = models.CharField(max_length=100, blank=True) # path to a shorter template for text-based (txt, facebook, twitter)-pushed notifications
    
    #TODO: Make text notifications work
    def send(self, template_dict=None):
        """
        Send the notification to the target Person by the method they have selected.
        """
        try:
            prefs = self.person.settings #load preferences
            # N, T, E, B - never, text, email, both
            if(prefs.updateMethod == "B"):
                self.send_email(self.person.user.email, template_dict)
                #self.send_text()
            elif(prefs.updateMethod == "E"):
                self.send_email(self.person.user.email, template_dict)
            elif(prefs.updateMethod == "T"):
                pass
                #self.send_text()    
        except Person.DoesNotExist:
            self.send_email(self.user.email, template_dict)
        
    
    def send_email(self, addr, template_dict=None):
        "Sends an email with this notification to the specified address."

        # build email from template
        html_content = render_to_string("alpha/notifications/" + self.template_path, {'ac':template_dict})
        text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
        
        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(self.subject, text_content, "livewith.us webmaster <webmaster@livewith.us>", [addr])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
    def send_text(self):
        "Sends a text message to the target person's cell"
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
