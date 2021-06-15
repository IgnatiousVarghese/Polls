from django import forms
from django.contrib.auth.models import Group
from .models import *

class Choiceform(forms.ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'

class Groupform(forms.ModelForm):
    class Meta:
        model = Questiongroup
        fields = '__all__'

class Questionform(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'