from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.models import Group, User
from register.forms import LoginForm
# Create your views here.

def register(request):
	if request.user.is_authenticated:
		return redirect('store')
	if request.method == "POST":
		form= RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			group = Group.objects.get(name='customer')
			user.groups.add(group)
			return redirect("/login")
	else:
		form = RegisterForm()		
	return render(request, "register/register.html", {"form":form})

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('profile')
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("/login")
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username = username, password = password)

		if user is not None:
			login(request, user)
			return redirect('store')

	else:
		form = LoginForm(request.POST)
	return render(request, "register/login.html", {"form":form})

def logoutPage(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('/login')
'''
class passwordReset(views.PasswordResetView):
	email_template_name = 'register/password-reset-email.html'
'''