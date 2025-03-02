from django import forms
import uuid
from django.contrib.auth.models import User # User model
from django.contrib.auth.forms import UserCreationForm # Forms for user
from ndio_app.models import Order, User_Detail 

# User registration form
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    # This class connects the fields of the mdel to the form
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserDetailForm(forms.ModelForm):
    id_number = forms.CharField(max_length=15)
    phone_number = forms.CharField(max_length=10)

    class Meta:
        model = User_Detail
        fields = ['id_number', 'phone_number']


class OrderForm(forms.ModelForm):
    CHOICES = [("House", "Free Standing House"),("Apartment", "Apartment/Complex"),("Estate", "Estate")]
    address_type = forms.ChoiceField(choices=CHOICES)
    apartment_name = forms.CharField(max_length=30) # This field can be empty
    apartment_floor = forms.IntegerField()
    apartment_unit = forms.IntegerField()
    estate_name = forms.CharField(max_length=30)
    estate_address = forms.CharField(max_length=50)
    address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=20)
    postal_code = forms.IntegerField()
      
    class Meta:
        model = Order
        fields = ['address_type', 'address', 'apartment_name', 'apartment_floor', 'apartment_unit', 'estate_name', 'estate_address', 'city', 'postal_code']

class PaymentForm(forms.Form):
    # amount is read only
    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'readonly': 'readonly'}))
    token = forms.CharField(widget=forms.HiddenInput())
    currency = forms.CharField(max_length=5, initial='ZAR', widget=forms.HiddenInput())
    name = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['token'].initial = str(uuid.uuid4())