from django.shortcuts import render, redirect
from users.forms import RegistrationForm, ProfileRegisterForm
from django.contrib import messages
# Create your views here.


def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		p_reg_form = ProfileRegisterForm(request.POST)
		if form.is_valid() and p_reg_form.is_valid():
			user = form.save()
			user.refresh_from_db()
			p_reg_form = ProfileRegisterForm(request.POST, instance=user.userprofile)
			p_reg_form.full_clean()
			p_reg_form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for username {username}!')
			return redirect('login')
	else:
		form = RegistrationForm()
		p_reg_form = ProfileRegisterForm()
	return render(request, 'users/register.html', {'form':form, 'p_reg_form': p_reg_form })
