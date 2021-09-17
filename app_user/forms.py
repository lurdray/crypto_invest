from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ("username", "password1", "password2")


