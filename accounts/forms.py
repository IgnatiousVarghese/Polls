from django.contrib.auth.models import User
from django import forms

class Registerform(forms.Form):
    username = forms.CharField(max_length= 100)
    password = forms.CharField(widget= forms.PasswordInput)
    c_password = forms.CharField(widget= forms.PasswordInput, required=True)

class Loginform(forms.Form):
    username = forms.CharField(max_length= 100)
    password = forms.CharField(widget= forms.PasswordInput)