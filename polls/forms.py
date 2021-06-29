from django import forms
from django.contrib.auth.models import Group
from .models import *


class Groupform(forms.ModelForm):
    class Meta:
        model = Questiongroup
        fields = [ 'group_name']

class Questionform(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        

class Choiceform(forms.ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'