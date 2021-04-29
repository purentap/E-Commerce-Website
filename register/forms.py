from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit

class RegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User 
		fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
	password = forms.PasswordInput()
	class Meta:
		model = User 
		fields = ["username", "password"]
