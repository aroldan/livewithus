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
from decimal import *
import random
import string
import os

from livewith.models import *
from livewith.utilities.dinner.models import *
from livewith.utilities.models import *

def pageview(request, page_name):
    "View a static page."
    try:
        return render_to_response("alpha/pages/%s.html" % page_name)
    except:
        raise Http404

def test_view(request, template_id):
    """
    Just returns the base template. For CSS testing.
    Test view is only enabled if DEBUG is true.
    """
    if(settings.DEBUG):
        return render_to_response("alpha/%s" % template_id)
    else:
        return render_to_response("alpha/error.html", {'exception_text': ('Operation not allowed')})
            
def index(request):
    """
    Index page. Redirects to default view for a house if logged in,
    or to the front page if not logged in.
    """
    if request.user.is_authenticated():
    # Do something for authenticated users.
        try:
            person = request.user.get_profile()
        except Person.DoesNotExist:
            return redirect(loginrequired)
        house = person.GetLastHouse()

        if house == None: #redirect to a house required page if there is no house
            return redirect(houserequired)

        return redirect(house) #otherwise, redirect to house home page
    else:
        return render_to_response("alpha/index.html", context_instance=RequestContext(request))

def signup_page(request):
    "Brings a user to the signup page."
    f = SignupForm()
    return render_to_response("alpha/signup/signup.html", {'form':f}, context_instance=RequestContext(request))

def faq(request):
    return render_to_response("alpha/pages/faq.html")
    
@login_required    
def apply_settings(request):
    house = request.user.get_profile().GetLastHouse()
    return redirect(house)

@login_required        
def houserequired(request):
    "Handler if a house is required for an action."
    return render_to_response("alpha/errors/house_required.html", context_instance=RequestContext(request))

def forgotpassword(request):
    return render_to_response("alpha/signup/forgotpassword.html")

def resetpassword(request):
    return render_to_response("alpha/signup/resetpassword.html")

@login_required
def createhouse(request):
    "Shows the house options screen, allowing a user to create or join a house"
    aclist = ApprovalCode.objects.filter(targetPerson=request.user.pk) # do any approval codes exist for this user?
    if aclist:
        clist = [(ac.inviteString, ac.house.name) for ac in aclist]
        acl = JoinHouseFormList(clist)
    else:
        acl = None
    
    jhf = JoinHouseForm() 
    return render_to_response("alpha/signup/house_options.html", {'jhform':jhf, 'aclist':acl}, context_instance=RequestContext(request))

def joinhouse_with_code(request, approval_code):
    try:
        ac = ApprovalCode.objects.get(inviteString=approval_code)
        f = SignupForm(initial={'email': ac.email})
        return render_to_response("alpha/signup/joinhouse_with_code.html", {'form' : f, 'ac': ac })        
    except ApprovalCode.DoesNotExist:
        return render_to_response("alpha/error.html", {'exception_text':('Invalid approval code.',)})
    
def signup_with_code(request, approval_code):
    "Handle a new user signing up, then redirect them to their dashboard"
    f = SignupForm(request.POST)
    
    try:
        ac = ApprovalCode.objects.get(inviteString=approval_code)
    except ApprovalCode.DoesNotExist: # return back to the form
        pass
    
    if f.is_valid():
        
        try:
            p = User.objects.get(email=f.cleaned_data['email'])
            return render_to_response("alpha/signup/user_exists.html", {'existing_user':p})
        except User.DoesNotExist:
            uLatest = User.objects.all().order_by('-pk')[0]
                
            u = User(first_name=f.cleaned_data['first_name'],
                     last_name=f.cleaned_data['last_name'],
                     username="u_%x" % (uLatest.pk+1) ,
                     is_active=True,
                     email=f.cleaned_data['email']
                     )
            u.set_password(request.POST['password'])
            u.save()
        
        person = Person(user=u) # create person
        person.save()
        
        ac.house.add_to_house(person) # add person to house
        
        ac.delete() # remove approval code
        
        u2 = authenticate(username=f.cleaned_data['email'], password=f.cleaned_data['password'])
        login(request, u2) # log us in
        
        welcome_alert = Alert()
        welcome_alert.person = person
        welcome_alert.house = ac.house
        welcome_alert.template_path = "welcome_alert.html"
        welcome_alert.save()
        
        return redirect('/lw')
    else:
        pass
        # go back and let people try entering the form correctly again
    return render_to_response("alpha/signup/joinhouse_with_code.html", {'form' : f, 'ac': ac })

@login_required
def joinhouse(request):
    "Join a house that already exists. Expects a form submission with an approval code"
    f = JoinHouseForm(request.GET)
    
    #TODO finish this!
    if f.is_valid():
        try:
            ac = ApprovalCode.objects.get(inviteString=f.cleaned_data['invite_code'])
            ac.house.add_to_house(request.user.get_profile())
            request.user.message_set.create(message="Welcome to %s!" % ac.house.name)
            ac.delete() # now delete approval code, since it's used
            return redirect(index)
        except ApprovalCode.DoesNotExist:
            f._errors['invite_code'] = [u"Invalid invite string!"]
            return render_to_response("alpha/signup/house_options.html", {'jhform':f}, context_instance=RequestContext(request))
    else:
        pass
    return render_to_response("alpha/signup/joinhouse.html")

@login_required
def do_createhouse(request):
    h = House(name=request.POST['hname'])
    h.save()
    person = request.user.get_profile()
    res = Residency(person=person, house=h, start_date=date.today(), end_date=date.max)
    res.save()
    
    alert = Alert()
    alert.person = person
    alert.house = h
    alert.template_path = "welcome_first_alert.html"
    alert.save()
    return redirect(index)

def loginrequired(request):
    "This view is called if a login is required to view a particular page."
    try:
        return render_to_response("alpha/login_required.html", {'next':request.GET['next']})
    except KeyError:
        return render_to_response("alpha/login_required.html")
    
def do_login(request):
    "Logs a user in."
    username = request.POST['username']
    password = request.POST['password']
    
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        try:
            return redirect(request.POST['next']) #if a next argument has been passed, redirect to that form
        except KeyError: 
            return redirect(index) #otherwise, redirect to the index
    else:
        return render_to_response("alpha/error.html", {'exception_text': ("Authentication failed.",)})

def do_logout(request):
    "Logs a user out."
    logout(request)
    return render_to_response("alpha/logged_out.html")

def house_redirect(request):
    #ToDo- this is a hacked fix for redirecting to the current house url. Right now this occurs in multiple places
    return redirect('/lw/%s/chatter' % request.POST.get('house_redirect'))

@login_required
def ack_alert(request, alert_id):
    """
    Handle an alert. Default/base alerts are handled here.
    
    This sets the alert to "acknowleged"
    """
    person = request.user.get_profile()
    try:
        alert = Alert.objects.get(pk=alert_id, acknowledged=False, person=person)
    except Alert.DoesNotExist: #if alert is not found, go home
         return render_to_response("alpha/error.html", {'exception_text': ("Alert not found or no permission.",)})
    
    alert.acknowledge() # ack the alert    
    if(alert.house):
        return redirect('/lw/%s/' % alert.house.pk)
    else:
        return redirect('/lw/')
    
@login_required
def refuse_payrequest_alert(request, alert_id):
    """
    Handle a refuse payment alert from settlements.
    
    Sets an alert to acknowledge and creates a new alert saying the payment was refused
    """
    person = request.user.get_profile()
    try:
        alert = Alert.objects.get(pk=alert_id, acknowledged=False, person=person)
    except Alert.DoesNotExist:
        return render_to_response("alpha/error.html", {'exception_text': ("Alert not found or no permission.",)})
    
    alert.acknowledge()
    
    refuse_alert = Alert()
    refuse_alert.person = Person.objects.get(id=alert.related_objects['creator'])
    refuse_alert.house = alert.house
    refuse_alert.related_objects = {'amount':alert.related_objects['amount'], 'description':alert.related_objects['description'], 'outcome':'refused payment', 'person':person.displayName(), 'person_id':person.pk, 'creator':refuse_alert.person.pk}
    refuse_alert.template_path = "payrequest_completed_owner_alert.html"
    refuse_alert.save()
    
    if (alert.house):
        return redirect('/lw/%s' % alert.house.pk)
    else:
        return redirect('/lw/')
    
@login_required
def accept_payrequest_alert(request, alert_id):
    person = request.user.get_profile()
    try:
        alert = Alert.objects.get(pk=alert_id, acknowledged=False, person=person)
    except Alert.DoesNotExist:
        return render_to_response("alpha/error.html", {'exception_text': ("Alert not found or no permission.",)})
    
    payform = PaymentForm({'amount':alert.related_objects['amount'], 'description':alert.related_objects['description']})
    payee = alert.related_objects['creator']
    return render_to_response('alpha/finances/report_payment.html', {'payform':payform, 'payee':payee, 'alert':alert, 'alert_boolean':"True", 'add':True}, context_instance=RequestContext(request))
    
@login_required
def complete_payrequest_alert(request, alert_id):
    person = request.user.get_profile()
    try:
        alert = Alert.objects.get(pk=alert_id, acknowledged=False, person=person)
    except Alert.DoesNotExist:
        return render_to_response("alpha/error.html", {'exception_text': ("Alert not found or no permission.",)})
    
    alert.acknowledge()
    
    accept_alert = Alert()
    accept_alert.person = Person.objects.get(id=alert.related_objects['creator'])
    accept_alert.house = alert.house
    accept_alert.related_objects = {'amount':alert.related_objects['amount'], 'description':alert.related_objects['description'], 'outcome':'completed payment', 'person':person.displayName(), 'person_id':person.pk, 'creator':accept_alert.person.pk}
    accept_alert.template_path = "payrequest_completed_owner_alert.html"
    accept_alert.save()
    
    payment = PaymentForm({})
    payment.data = request.POST.copy()
    
    if request.method == 'POST' and payment.is_valid():
        #Save payment data as a settlement transaction
    
        settlement = Settlement()
        settlement.creator = person
        settlement.purchase_date = datetime.now()
        settlement.house = alert.house
        settlement.description = payment.cleaned_data['description']
        settlement.banker = Person.objects.get(id=request.POST['payment_to'])
        settlement.save()
        
        debt = Debt()
        debt.person = Person.objects.get(id=request.POST['payment_to'])
        debt.value = request.POST['amount']
        debt.transaction = settlement
        debt.save()
    
    
    return redirect('/lw/')

@login_required   
@house_required 
def dashboard(request, house_id):
    """
    Dashboard Page: Contains today's chatter, alerts, and quick view finances
    """
    
    house = House.objects.get(id=house_id)
    
    #CHATTER
    today = datetime.now()
    
    sticky_chats = HMChatter.objects.filter(house=house_id).filter(sticky=True).order_by('-timeModified')
    todays_chats = HMChatter.objects.filter(house=house_id).filter(timeModified__year=today.year).filter(timeModified__month=today.month).filter(timeModified__day=today.day).filter(sticky=False).order_by('-timeModified')
    older_chats = HMChatter.objects.filter(house=house_id).exclude(timeModified__day=today.day).filter(sticky=False, parent=None).order_by('-timeModified')
    older_chat_count = older_chats.count()

    form = HMChatterForm()
    return render_to_response('alpha/dashboard.html', {'older_chat_count': older_chat_count, 'sticky_chats':sticky_chats, 'todays_chats':todays_chats, 'older_chats':older_chats[:5], 'form':form}, context_instance=RequestContext(request))

@login_required
@house_required
def delete_chatter(request, house_id, chatter_id):
    """
    Deletes a chatter object.
    """
    chatter = HMChatter.objects.get(pk=chatter_id)
    person = request.user.get_profile()
    if (chatter.house.pk == int(house_id)) and (chatter.creator.pk == person.pk or not isinstance(chatter.creator.downcast(), Person)):
        #delete children as well
        for c in chatter.child_set.all():
            c.delete()
        
        chatter.delete()
        return redirect(index)
    else:
        return redirect(index) # redirect to index if mismatched house or person
    
@login_required
@house_required
def stick_chatter(request, house_id, chatter_id):
    """
    Stickies a chatter object.
    """
    chatter = HMChatter.objects.get(pk=chatter_id)
    if chatter.house.pk == int(house_id):
        chatter.sticky = True
        chatter.save()
        
        return redirect(index)
    else:
        return redirect(index) # redirect to index if mismatched house or person
    
@login_required
@house_required
def unstick_chatter(request, house_id, chatter_id):
    """
    Unstickies a chatter object.
    """
    chatter = HMChatter.objects.get(pk=chatter_id)
    if chatter.house.pk == int(house_id):

        chatter.sticky = False
        chatter.save()
        
        return redirect(index)
    else:
        return redirect(index) # redirect to index if mismatched house or person

def more_chatter(request, house_id):
    "Loads more chatter items, with the number specified by the POST or GET variable num."
    
    # try POST, then GET, then a default of 2
    try:
        end = int(request.POST['end'])
    except KeyError:
        try:
            end = int(request.GET['end'])
        except KeyError:
            end = 2 
    
    form = HMChatterForm()
        
    today = datetime.now()
          
    older_chats = HMChatter.objects.filter(house=house_id).filter(sticky=False, parent=None).exclude(timeModified__day=today.day).order_by('-timeModified')[5:end]
    
    return render_to_response('alpha/chatter/more_chats.html', {'chats':older_chats, 'form': form}, context_instance=RequestContext(request))

@login_required
def chathandler(request):
    """
    Handles all chatter posts by creating new Chatter objects
    """
    house = House.objects.get(pk=request.POST['house'])
    person = request.user.get_profile()
    if request.method == 'POST':
        chat = HMChatterForm({})
        chat.data = request.POST.copy()
        chat.data['creator'] = person.pk
        
        if chat.is_valid() and chat.cleaned_data['text'] != "":
            if(chat.cleaned_data['as_poll']):
                p = HMPoll(creator=person, house=chat.cleaned_data['house'], sticky=False, parent=chat.cleaned_data['parent'], text="New Poll", publicly_editable=False)
                p.set_text(chat.cleaned_data['text'])
                p.save()
                p.create_options_from_text(chat.cleaned_data['text'])
                
                # all done, now redirect to dashboard
                
                if chat.cleaned_data['parent']:
                    parent_chat = chat.cleaned_data['parent']
                    parent_chat.timeModified = datetime.now()
                    parent_chat.save()
                
                p.notify()
            else:
                c = chat.save(False)
                c.save()
                c.notify() # push notifications

                if chat.cleaned_data['parent']:
                    parent_chat = chat.cleaned_data['parent']
                    parent_chat.timeModified = datetime.now()
                    parent_chat.save()

                
                
                #TODO- this is a hacked fix for redirecting to the current house url. Right now this occurs in multiple places
            return redirect('%s' % house.get_absolute_url())
        else:
            return redirect(index)
    else:
        return redirect(index)

@login_required
def pollhandler(request):
    person = request.user.get_profile()
    house = House.objects.get(pk=request.POST['house_id'])
    if request.method == 'POST':
        poll = HMPoll.objects.get(id=int(request.POST['poll_id']))
        poll.delete_responses(person)
        votes = request.POST.getlist('poll_choice')
        for vote in votes:
            response = PollResponse()
            response.person = person
            response.vote = PollOption.objects.get(id=int(vote))
            response.save()
        return redirect('%s' % house.get_absolute_url())
    else:
        return redirect('%s' % house.get_absolute_url())


@login_required
def savewikihandler(request):
    house = House.objects.get(pk=request.POST['house'])
    
    chat = HMChatter.objects.get(id=request.POST['chat'])
    chat.text = request.POST['text']
    chat.timeModified = datetime.now()
    chat.save()
    return redirect('%s' % house.get_absolute_url())

@login_required
@house_required
def finances(request, house_id, sort_view):
    """
    Financial page displays a list of some financial transactions
    """
    person = request.user.get_profile()
    house = House.objects.get(pk=house_id)
    #get list of purchases for this house, sorted by descending purchase date
    purchases = person.get_transactions(house).order_by('-purchase_date')
    
    if sort_view == "purchases":
        purchases = purchases.filter(creator=person)
    elif sort_view == "debts":
        purchases = purchases.exclude(creator=person)
    else:
        pass #use default sorting
    
    plist = list(purchases) # we have to convert this to a list to append debt amounts
    for p in plist:
        p.debt = p.get_debt(person)
    
    return render_to_response('alpha/finances/finances.html', {'purchases':plist}, context_instance=RequestContext(request))

@login_required
@house_required
def finance_detail_view(request, house_id, transaction_id):
    """
    Returns details for a particular purchase.
    """
    purchase = HMTransaction.objects.get(pk=transaction_id)
    return render_to_response('alpha/finances/finance_details.html', {'purchase':purchase}, context_instance=RequestContext(request))

@login_required
@house_required
def request_payment(request, house_id):
    house = House.objects.get(id=house_id)
    payform = PaymentForm()
    return render_to_response('alpha/finances/request_payment.html', {'payform':payform}, context_instance=RequestContext(request))
    
@login_required
@house_required
def request_payment_handler(request, house_id):
    house = House.objects.get(id=house_id)
    person = request.user.get_profile()
    if request.method == 'POST':
        payment = PaymentForm({})
        payment.data = request.POST.copy()
        
        requestee = Person.objects.get(id=request.POST['payment_from']).displayName()
        
        owner_alert = Alert()
        owner_alert.person = person
        owner_alert.house = house
        owner_alert.related_objects = {'amount':str(payment.data['amount']), 'description':payment.data['description'], 'person':requestee, 'person_id':person.pk, 'creator':person.pk}
        owner_alert.template_path = "payrequest_pending_owner_alert.html"
        owner_alert.save()
        
        reciever_alert = Alert()
        reciever_alert.person = Person.objects.get(id=request.POST["payment_from"])
        reciever_alert.house = house
        reciever_alert.related_objects = {'amount': str(payment.data['amount']), 'description':payment.data['description'], 'person':person.displayName(), 'person_id':person.pk, 'creator':person.pk}
        reciever_alert.template_path = "payrequest_pending_reciever_alert.html"
        reciever_alert.save()

        #TODO add completed message to redirect
        message = "Payment request has been sent"
        return redirect('%s' % house.get_absolute_url())
    else:
        payform = PaymentForm()
        return render_to_response('alpha/finances/request_payment.html', {'payform':payform}, context_instance=RequestContext(request))
    
    
@login_required
@house_required
def report_payment(request, house_id):
    house = House.objects.get(id=house_id)
    payform = PaymentForm()
    return render_to_response('alpha/finances/report_payment.html', {'payform':payform, 'add':True}, context_instance=RequestContext(request))

@login_required
@house_required
def report_payment_handler(request, house_id):
    house = House.objects.get(id=house_id)
    person = request.user.get_profile()
    
    payment = PaymentForm({})
    payment.data = request.POST.copy()
    if request.method == 'POST' and payment.is_valid():
        #Save payment data as a settlement transaction

        settlement = Settlement()
        settlement.creator = person
        settlement.purchase_date = datetime.now()
        settlement.house = house
        settlement.description = payment.cleaned_data['description']
        settlement.banker = Person.objects.get(id=request.POST['payment_to'])
        settlement.save()
        
        debt = Debt()
        debt.person = Person.objects.get(id=request.POST['payment_to'])
        debt.value = request.POST['amount']
        debt.transaction = settlement
        debt.save()
        
        return redirect('%sfinances/all' % house.get_absolute_url())
    else:
        payform = PaymentForm()
        return render_to_response('alpha/finances/report_payment.html', {'payform':payform}, context_instance=RequestContext(request))
    

@login_required
@house_required
def edit_payment_handler(request, settlement_id):
    settlement = Settlement.objects.get(id=request.POST['settlement'])
    settlement.description = request.POST['description']
    settlement.banker = Person.objects.get(id=request.POST['payment_to'])
    settlement.save()
    
    debt = Debt.objects.get(transaction=settlement)
    debt.value = request.POST['amount']
    debt.save()
    
    alert = Alert()
    alert.house = settlement.house
    alert.person = settlement.banker
    alert.template_path = "settlement_change_alert.html"
    url = settlement.house.get_absolute_url() + "finances/edit/" + str(settlement.pk)
    alert.related_objects = {'creator':settlement.creator, 'url':url, 'date':settlement.purchase_date}
    alert.save()
    
    return redirect('%sfinances/all' % house.get_absolute_url())
                               
@login_required    
@house_required
def add_transaction(request, house_id):
    form = PurchaseForm({'purchase_date': datetime.now().strftime("%m/%d/%Y")})
    house = House.objects.get(pk=house_id)
    vendor_list = []
    vendors = Vendor.objects.all()
    for vendor in vendors:
        vendor_list.append(str(vendor.name))
    return render_to_response('alpha/finances/add_transaction.html', {'form':form, 'vendors':vendor_list, 'add':True }, context_instance=RequestContext(request))

@login_required
@house_required    
def edit_transaction(request, house_id, transaction_id):
    try:
        purchase = HMTransaction.objects.get(id=transaction_id).downcast()
        
        pDebts = {}
        for d in purchase.get_debts():
            pDebts[d.person.pk] = d.amount()
            
        form = PurchaseForm({'purchase_date': purchase.purchase_date.strftime("%m/%d/%Y"), 'vendorText':purchase.vendor.name, 'description':purchase.description, 'amount':purchase.amount()})
        vendor_list = []
        vendors = Vendor.objects.all()
        for vendor in vendors:
            vendor_list.append(str(vendor.name))
        return render_to_response('alpha/finances/add_transaction.html', {'pdebts':pDebts, 'form':form, 'purchase':purchase, 'vendors':vendor_list, 'add':False }, context_instance=RequestContext(request))
    except Purchase.DoesNotExist:
        settlement = Settlement.objects.get(id=purchase_id)
        payer = settlement.banker
        form = PaymentForm({'amount':settlement.amount(), 'description':settlement.description})
        return render_to_response('alpha/finances/report_payment.html', {'payform':form, 'payer':payer, 'add':False, 'settlement':settlement.pk}, context_instance=RequestContext(request))


@login_required
@house_required
def new_purchase_handler(request, house_id):
    house = House.objects.get(pk=house_id)
    
    person = request.user.get_profile()
    
    purchase = PurchaseForm({})
    purchase.data = request.POST.copy()
    purchase.data['creator'] = person.pk
    
    if request.method == 'POST' and purchase.is_valid():
        #TODO- This whole piece sort of hacked together. Needs cleanup work
        
        # now locate the proper vendor, and create it if needed
        try:
            v = Vendor.objects.get(name=purchase.cleaned_data['vendorText'])
        except Vendor.DoesNotExist: # if vendor does not exist
            v = Vendor(name=purchase.cleaned_data['vendorText'])
            v.save()
            
        amount = purchase.cleaned_data['amount']
        
        members = [int(val) for val in request.POST.getlist('included')]

        # catch transactions that are too big
        if amount > 100000000000:
            #TODO - add the "included people" thing as a Django form and push errors there
            request.user.message_set.create(message="Whoa there, Mr. Moneybags. Please enter a smaller amount.")
            return render_to_response('alpha/finances/add_transaction.html', {'form':purchase, 'add':True }, context_instance=RequestContext(request))
        
        transaction = purchase.save(commit=False) # get     transaction object without saving to DB
        transaction.vendor = v # set vendor
        transaction.house = house # set house
        transaction.save() # now save transaction
        
        # create debts
        for member in members:
            debt = Debt()
            debt.person = Person.objects.get(id=member)
            debt.transaction = transaction
            debt.value = purchase.data['amount_%d' % member].strip(" $").replace(',','')
            debt.time = purchase.data['purchase_date']
            debt.save()
            
        #TODO- this is a hacked fix for redirecting to the current house url. Right now this occurs in multiple places
        return redirect('%sfinances/all' % house.get_absolute_url())
    else:
        #TODO - add the "included people" thing as a Django form and push errors there
        request.user.message_set.create(message="Item could not be submitted. Please ensure all fields are filled in and that at least one participant is included.")
        return render_to_response('alpha/finances/add_transaction.html', {'form':purchase, 'add':True }, context_instance=RequestContext(request))

@login_required
@house_required
def edit_purchase_handler(request, house_id, purchase_id):
    house = House.objects.get(pk=int(house_id))
    
    person = request.user.get_profile()
    
    purchase = PurchaseForm({})
    purchase.data = request.POST.copy()
    purchase.data['creator'] = person.pk
    
    if request.method == 'POST' and purchase.is_valid():
        #TODO- This whole piece sort of hacked together. Needs cleanup work
        transaction = Purchase.objects.get(pk=int(purchase_id)) # find existing transaction
        
        #locate the proper vendor, and create it if needed
        try:
            v = Vendor.objects.get(name=purchase.cleaned_data['vendorText'])
        except Vendor.DoesNotExist: # if vendor does not exist
            v = Vendor(name=purchase.cleaned_data['vendorText'])
            v.save()
        
        #update transaction fields
        transaction.description = purchase.cleaned_data['description']
        transaction.purchase_date = purchase.cleaned_data['purchase_date']
        transaction.vendor = v # set vendor
        transaction.save() # now save transaction
        
        # now remove old debts
        debts = transaction.get_all_debts()
        for debt in debts:
            debt.delete() # remove old debts
            
        #get amount and new members
        amount = purchase.cleaned_data['amount']
        
        members = [int(val) for val in request.POST.getlist('included')]
        
        # create new debts
        for member in members:
            debt = Debt()
            debt.person = Person.objects.get(id=member)
            debt.transaction = transaction
            debt.value = purchase.data['amount_%d' % member].strip(" $").replace(',','')
            debt.time = purchase.data['purchase_date']
            debt.save()
            
        #TODO- this is a hacked fix for redirecting to the current house url. Right now this occurs in multiple places
        return redirect('%sfinances/all' % house.get_absolute_url())
    else:
        form = HMChatterForm()
        return render_to_response('alpha/finances/add_transaction.html', {'form':purchase }, context_instance=RequestContext(request))

@login_required
@house_required
def delete_transaction_handler(request, house_id, transaction_id):
    #TODO- I don't think this is the safe way of doing this, but I don't know what the safe way is...
    try:
        purchase = Purchase.objects.get(id=transaction_id)
        house = House.objects.get(pk=int(house_id))
        debts = Debt.objects.filter(transaction=transaction_id)
        for debt in debts:
            debt.delete()
        purchase.delete()
        return redirect('%sfinances/all' % house.get_absolute_url())
    except:
        try:
            purchase = Settlement.objects.get(id=transaction_id)
            house = House.objects.get(pk=int(house_id))
            debts = Debt.objects.filter(transaction=transaction_id)
            for debt in debts:
                debt.delete()
            purchase.delete()
            return redirect('%sfinances/all' % house.get_absolute_url())
        except:
            return render_to_response("alpha/error.html", {'exception_text': ("Transaction does not exist",)})

        
def signup(request):
    f = SignupForm(request.POST)
    
    if f.is_valid():      
        #first, see if a user with this email already exists
        try:
            p = User.objects.get(email=f.cleaned_data['email'])
            return render_to_response("alpha/signup/user_exists.html", {'existing_user':p})
        except User.DoesNotExist: # if not, continue the signup process
            uLatest = User.objects.all().order_by('-pk')[0]
            
            u = User(first_name=f.cleaned_data['first_name'],
                     last_name=f.cleaned_data['last_name'],
                     username="u_%x" % (uLatest.pk+1) ,
                     is_active=True,
                     email=f.cleaned_data['email']
                     )
            u.set_password(request.POST['password'])
            u.save()
            p = Person(user=u)
            p.save()
    
            user_loggedin = authenticate(username=u.username, password=request.POST['password']) #user must be authenticated per django constraints
            login(request, user_loggedin) # now log the user in
            
            jhf = JoinHouseForm()
            
            return render_to_response('alpha/signup/house_options.html', {'jhform':jhf, 'signup':True}, context_instance=RequestContext(request))
    else:
        return render_to_response('alpha/signup/signup.html', {'form':f})
        
    
def signuphandler(request):
    "Handle a new user signing up, then redirect them to their dashboard"
    user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
    user.save()
    person = Person(user=user)
    person.save()
    return HttpResponseRedirect('/dashboard')

@login_required
def apply_person_settings(request):
    "Apply settings for a person."
    
    # create a user preferences form from the POST data
    f = UserPreferencesForm(request.POST, request.FILES)

    if f.is_valid():
        uprefsNew = f.save(commit=False)
        person = request.user.get_profile()
        uprefsOld = person.settings # load old settings
        
        #copy fields from new settings
        #TODO: is there a better way to do this? this seems a bit backwards.
        uprefsOld.updateMethod = uprefsNew.updateMethod
        uprefsOld.cell_provider = uprefsNew.cell_provider
        uprefsOld.phoneNumber = uprefsNew.phoneNumber
        
        if f.cleaned_data['password'] != "":
            request.user.set_password(f.cleaned_data['password'])
            request.user.save()
        
        try:
            if f.files['avatar']:
                uploadedImage = f.cleaned_data['avatar']
                
                person.upload_avatar(uploadedImage.name.split(".")[-1], uploadedImage)
                person.save()
        except KeyError: # if no avatar is uploaded
            pass
        
        uprefsOld.save() # now update old settings
        request.user.message_set.create(message="Changes applied!")
        return redirect(person_settings)
    else:
        return redirect(person_settings)
    
@login_required
def person_settings(request, form=None):
    "Manage settings for an individual."
    person = request.user.get_profile()
    
    if form: # use imported form if set
        f = form
    else:
        f = UserPreferencesForm(instance=person.settings);
    
    return render_to_response('alpha/settings.html', {'form':f}, context_instance=RequestContext(request))

@login_required
@house_required
def house_settings(request, house_id, form=None):
    "Manage settings for a house."
    if form:
        f = form
    else:
        f = InviteHousematesForm()

    house = House.objects.get(pk=house_id)
    settings = House.objects.get(id=house_id).settings    
    sf = HouseSettingsForm({"time_zone":settings.time_zone, 'house_name':house.name})
        
    house = House.objects.get(id=house_id)
    active_settings = UtilityHouseSettings.objects.filter(house=house).filter(active=True)
    #inactive_settings = UtilityHouseSettings.objects.filter(house=house).exclude(active=True)
    inactive_utilities = []

    utilities = HMUtility.objects.all()
    for utility in utilities:
        setting = UtilityHouseSettings.objects.filter(house=house).filter(utility=utility)
        try:
            if setting[0].active != True:
                inactive_utilities.append(utility)
        except:
            inactive_utilities.append(utility)

    return render_to_response('alpha/housesettings.html', {'invite_form':f, 'settings_form':sf, 'active_settings':active_settings, 'inactive_utilities':inactive_utilities}, context_instance=RequestContext(request))


@login_required
@house_required
def apply_house_settings(request, house_id):
    "Manage settings for a house."
    f = HouseSettingsForm(request.POST, request.FILES)

    if f.is_valid():
        uprefsNew = f.save(commit=False)
        house = House.objects.get(id=house_id)
        uprefsOld = house.settings # load old settings
        
        #copy fields from new settings
        #TODO: is there a better way to do this? this seems a bit backwards.
        uprefsOld.time_zone = uprefsNew.time_zone
        
        if f.cleaned_data['house_name'] != "":
            house.name = f.cleaned_data['house_name']
            house.save()
            
         
        try:
            if f.files['avatar']:
                uploadedImage = f.cleaned_data['avatar']
                
                house.upload_avatar(uploadedImage.name.split(".")[-1], uploadedImage)
                house.save()
        except KeyError: # if no avatar is uploaded
            pass
        
        uprefsOld.save() # now update old settings
        request.user.message_set.create(message="Changes applied!")
        return redirect(house_settings, house_id)
    else:
        return redirect(house_settings, house_id)

@login_required
@house_required
def invite_housemates(request, house_id):
    f = InviteHousematesForm(request.POST)
    if f.is_valid():
        #TODO actually send an email here
        
        #pull in a house
        house = House.objects.get(pk=house_id)
        
        #generate a 10 char invitation code
        inviteString = "".join([random.choice(string.ascii_letters) for i in range(10)]) # random 10 char string
        
        #first, check if the user is already registered
        try:
            test_user = User.objects.get(email=f.cleaned_data['email'])
            request.user.message_set.create(message="That person already has a livewith.us account!")
            c = ApprovalCode(house=house, person=request.user.get_profile(), inviteString=inviteString, targetPerson=test_user)
        except User.DoesNotExist:
            # normal case, the user does not exist, so let's send an invitation
            c = ApprovalCode(house=house, person=request.user.get_profile(), inviteString=inviteString, email=f.cleaned_data['email'])
            
        c.save()
        c.dispatch_email()

        #TODO evaluate if django messaging is enough or if we need to do more
        request.user.message_set.create(message="Invitation sent!") # Uses the soon-to-be
        
        return redirect(house_settings, house_id) #redirect back to the settings page
    else:
        house = House.objects.get(pk=house_id)
        settings = House.objects.get(id=house_id).settings    
        sf = HouseSettingsForm({"time_zone":settings.time_zone, 'house_name':house.name})
        return render_to_response('alpha/housesettings.html', {'invite_form': f, 'settings_form':sf}, context_instance=RequestContext(request))



    
    
                      
