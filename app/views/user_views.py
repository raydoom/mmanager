from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import models, authenticate
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

import logging, os, configparser, json

from ..utils.common_func import auth_controller, log_record


# 用户登陆
def login(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		if authenticate(username=username, password=password):
			request.session['islogin'] = True
			request.session['username'] = username
			return redirect("/index/")
		else:
			message = 'username or password error!'
			return render(request, 'login.html', {"message": message})
	return render(request, 'login.html')

# 用户设置
@auth_controller
def settings(request):
	username = request.session.get('username')
	userinfo = models.User.objects.get(username=username)
	return render(request, 'settings.html', {'userinfo': userinfo})

# 修改密码
@auth_controller
def passwordchange(request):
	if request.method == 'POST':
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
@auth_controller
def logout(request):
	request.session.flush()
	return redirect("/index/")


# 用户注册
def register(request):
	pass
	return redirect("/index/")

