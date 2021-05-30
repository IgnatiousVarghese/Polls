from django import forms
from .models import Choice, Question

class Choiceform(forms.ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'