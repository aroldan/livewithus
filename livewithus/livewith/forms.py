from django import forms
from django.forms import ModelForm
from livewith.models import User, Purchase, Settlement, House, HMChatter, HMTransaction, UserPreferences, HousePreferences

class LWCurrencyField(forms.DecimalField):
    "Custom Currency field; strips $ and , out"
    def __init__(self, max_value=None, min_value=None, max_digits=None, *args, **kwargs):
        kwargs["decimal_places"] = 2
        forms.DecimalField.__init__(self, max_value, min_value, max_digits, *args, **kwargs)
    
    def to_python(self, value):
        if value is None: return None
        new_value = value.strip(" $").replace(",","")
        return forms.DecimalField.to_python(self, new_value)

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(max_length=30, widget=forms.PasswordInput, label="Password")
    password_verify = forms.CharField(max_length=30, widget=forms.PasswordInput, label="Verify Password")
    
    #TODO: remove auth code for signup for final version
    auth_code = forms.CharField(max_length=30, label="Authorization Code")

    def clean_password(self):
        try:
            if self.data['password'] != self.data['password_verify']:
                raise forms.ValidationError('Passwords are not the same')
            return self.data['password']
        except KeyError:
            raise forms.ValidationError('Passwords do not match!')
    
    def clean(self,*args, **kwargs):
        self.clean_password()
        
        if self.data['auth_code'] != "steak":
            raise forms.ValidationError("Authorization code is incorrect or not provided.")
            
        return super(SignupForm, self).clean(*args, **kwargs)


class HouseSettingsForm(ModelForm):
    house_name = forms.CharField(max_length=30, label="House Name")
    avatar = forms.ImageField(label = "House Avatar", required=False)
    
    class Meta:
        model = HousePreferences

class InviteHousematesForm(forms.Form):
    email = forms.EmailField(label="Housemate's Email Address")
    
class JoinHouseForm(forms.Form):
    invite_code = forms.CharField(max_length=10, label="Invitation Code")
    
class JoinHouseFormList(forms.Form):
    "JoinHouseForm, but creates a dropdown list instead."
    invite_code = forms.ChoiceField()
    
    def __init__(self, clist, *args, **kwargs):
        super(JoinHouseFormList, self).__init__(*args, **kwargs)
        self.fields['invite_code'].choices = clist
        
class PaymentForm(forms.Form):
    amount = forms.DecimalField()
    description = forms.CharField(required=False)

class UserPreferencesForm(ModelForm):
    """"
    Form for individual user preferences.
    """
    phoneNumber = forms.CharField(label="Cell Phone (no dashes)", required=False)
    avatar = forms.ImageField(label = "User Avatar", required=False)
    
    password = forms.CharField(max_length=30, widget=forms.PasswordInput, label="Change password", required=False)
    password_verify = forms.CharField(max_length=30, widget=forms.PasswordInput, label="Verify new password", required=False)
    
    def clean_password(self):
        "Ensure the passwords match if they are set."
        if self.data['password'] != "" and self.data['password'] != self.data['password_verify']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']
    
    def clean(self,*args, **kwargs):
        self.clean_password()        
            
        return super(UserPreferencesForm, self).clean(*args, **kwargs)
    
    class Meta:
        model = UserPreferences
        
class HouseForm(ModelForm):
    class Meta:
        model = House

class UserForm(ModelForm):
    class Meta:
        model = User   
        
class HMChatterForm(ModelForm):
    as_poll = forms.BooleanField(required=False)
    
    class Meta:
        model = HMChatter

class HMTransactionForm(ModelForm):
    class Meta:
        model = HMTransaction
        
class SettlementForm(ModelForm):
    class Meta:
        model = Settlement
        
class PurchaseForm(ModelForm):
    """
    Form to create a purchase. This appends "vendortext" as a field, which
    is populated with the name of the vendor as a text field. Upon submission,
    it is used to create a new vendor object.
    """
    amount = LWCurrencyField()
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 2}))
    
    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['vendorText'] = forms.CharField(max_length=35, label="Vendor")
        
    def ensure_people_checked(self):
        "Ensure that at least one person is checked"
        try:
            self.data['included']
        except KeyError:
            raise forms.ValidationError('At least one person must be checked.')
        
    def clean(self,*args, **kwargs):
        self.ensure_people_checked()
        return super(PurchaseForm, self).clean(*args, **kwargs)
    
    class Meta:
        model = Purchase
        exclude = ('vendor',) # we don't need the vendor field, since we're using text
                