from django import forms
from django.contrib.auth.models import User
from Profile.models import UserProfile
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password1',
			'password2'
			]
			

class ProfileRegisterForm(forms.ModelForm):
	class Meta:	
		model = UserProfile
		username = None
		fields = ['nickname']