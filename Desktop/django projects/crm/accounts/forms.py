from django import forms
from accounts.models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import *

class createform(forms.ModelForm):
    class Meta:
        model=Order
        fields="__all__"

class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields="__all__"
        exclude=["customer"]

class registerform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2','email']

class loginown(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
