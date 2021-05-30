from django.contrib.auth.models import User
from django import forms

class Registerform(forms.ModelForm):
    c_password = forms.CharField()
    class Meta:
        model = User
        fields = ['username', 'password']

class Loginform(forms.Form):
    username = forms.CharField(max_length= 100)
    password = forms.CharField(max_length= 100)