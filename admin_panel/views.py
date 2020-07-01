from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import datetime
# Create your views here.
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import *
from .forms import *
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from django.utils.decorators import method_decorator

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from .password_reset_form import MyPasswordResetForm
from .models import *
from registration.models import *
from django.db.models import Sum
from django.contrib.auth import update_session_auth_hash
from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import date

import csv
from django.http import HttpResponse
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractYear

import itertools


class AdminLoginView(View):
	def get(self, request):
		form = LoginForm
		if request.user.is_authenticated:
			return HttpResponseRedirect('/admin/panel/home/')

		return render(request, 'admin_panel/accounts/login.html', {'form': form})

	def post(self, request):
		form = LoginForm(request.POST or None)
		if form.is_valid():
			user = User.objects.get(email=request.POST['email'], is_staff=True, is_superuser=True,)
			login(request, user)
			return HttpResponseRedirect('/admin/panel/home')

		return render(request, 'admin_panel/accounts/login.html', {'form': form})


class LogoutView(View):

	def get(self,request):
		logout(request)
		return HttpResponseRedirect('/admin/panel/login/')


class ResetPasswordView(auth_views.PasswordResetView):
	 form_class = MyPasswordResetForm


class ChangePasswordView(View):

	def get(self, request):
		form = ChangePasswordForm(user=request.user)
		return render(request, 'admin_panel/accounts/change_password.html', {'form': form})

	def post(self, request):
		user = request.user
		print(request.POST)
		form = ChangePasswordForm(request.POST or None, user=request.user)

		if form.is_valid():
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
			update_session_auth_hash(request, form.user)
			# messages.success(request, 'Your password have been changed successfully. Please login again to access account')
			return HttpResponseRedirect('/admin/panel/login/')
		return render(request, 'admin_panel/accounts/change_password.html', {'form': form})



class AdminHomeView(View):

	def get(self, request):
		
		return render(request, 'admin_panel/home.html')


class AdminProfileView(View):

	def get(self, request):

		form = AdminProfileEditForm
		user =request.user


		rs_user = RegisteredUser.objects.get(user=user)

		context = {

			'form': form,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'email': user.email,
			'mobile_number': rs_user.mobile,
			# 'profile_image': rs_user.country_code,
			# 'cover_image': user.cover_image,
			'country_code': rs_user.country_code
		}

		return render(request, 'admin_panel/accounts/admin_profile.html', context)


class AdminProfileEditView(View):
	def get(self, request):
		form = AdminProfileEditForm
		user = request.user
		rs_user = RegisteredUser.objects.get(user=user)

		context = {

			'form': form,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'email': user.email,
			'mobile_number': rs_user.mobile,
			# 'profile_image': rs_user.country_code,
			# 'cover_image': user.cover_image,
			'country_code': rs_user.country_code
		}

		return render(request, 'admin_panel/accounts/admin_profile_change.html', context)

	def post(self, request):
		data = request.POST
		user = request.user
		form = AdminProfileEditForm(request.POST or None, user=request.user)
		if form.is_valid():


			profile_image = request.FILES.get('profile_image')
			cover_image = request.FILES.get('cover_image')

			user.email = form.cleaned_data['email']
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.mobile_number = form.cleaned_data['mobile_number']

			if profile_image is not None:
				user.profile_image = profile_image
			if cover_image is not None:
				user.cover_image = cover_image

			user.save()
			return HttpResponseRedirect('/admin/panel/admin_profile/')

		context = {

			'form': form,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'email': user.email,
			'mobile_number': rs_user.mobile,
			# 'profile_image': rs_user.country_code,
			# 'cover_image': user.cover_image,
			'country_code': rs_user.country_code
		}

		return render(request, 'admin_panel/accounts/admin_profile_change.html', context)



