from django import forms
from django.forms import ModelForm

from .models import Task


class TaskForm(forms.ModelForm):
	title = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Add new task...'}))
	desc = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'enter description...'}))
	class Meta:
		model = Task
		fields = ['title' ,'desc', 'completed']

class updateForm(forms.ModelForm):
	title = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'edit current task...'}))
	desc = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'edit current task...'}))
	class Meta:
		model = Task
		fields = ['title' ,'desc', 'completed']
