from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import models, authenticate
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
import logging, os, configparser, json

from ..utils.common_func import auth_controller, log_record


# 用户登陆
class Login(View):
	def get(self, request):
		return render(request, 'login.html')

	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		if authenticate(username=username, password=password):
			request.session['islogin'] = True
			request.session['username'] = username
			return redirect("/index/")
		else:
			message = 'username or password error!'
			return render(request, 'login.html', {"message": message})

# 用户设置
class Settings(View):
	def get(self, request):
		username = request.session.get('username')
		userinfo = models.User.objects.get(username=username)
		return render(request, 'settings.html', {'userinfo': userinfo})

# 修改密码
class Change_Password(View):
	def get(self, request):
		return render(request, 'password_change_form.html')

	def post(self, request):
		username = request.session.get('username')
		old_password = request.POST.get('old_password')
		new_password = request.POST.get('new_password')
		confirm_new_password = request.POST.get('confirm_new_password')
		if new_password != confirm_new_password:
			message = 'confirm_new_password is not match'
			return render(request, 'password_change_form.html', {"message": message})
		if authenticate(username=username, password=old_password):
			models.User.objects.filter(username=username).update(password=make_password(new_password, None, 'pbkdf2_sha256'))
			return render(request, 'password_change_done.html')
		else:
			message = 'Old password is wrong'
			return render(request, 'password_change_form.html', {"message": message})
		return render(request, 'password_change_form.html')


# 用户退出
class Sign_Out(View):
	def get(self, request):
		request.session.flush()
		return redirect("/index/")


# 用户注册
class Register(View):
	def get(self, request):
		return redirect("/index/")
