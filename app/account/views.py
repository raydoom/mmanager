# coding=utf8

import os
import logging
import json
import configparser
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from app.account.models import User
from app.utils.common_func import auth_login_required
from app.utils.common_func import log_record
from app.utils.paginator import paginator_for_list_view

# 用户登陆
class LoginView(View):
	def get(self, request):
		return render(request, 'login.html')
		
	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = User.objects.filter(username=username).first()
		if user:
			if check_password(password, user.password):
				request.session['islogin'] = True
				request.session['username'] = username
				request.session['user_id'] = user.user_id
				request.session['role'] = user.role
				return redirect("/docker/container_list")
			else:
				message = 'username or password error!'
				context = {"message": message}
				return render(request, 'login.html', context)

		else:
			message = 'username or password error!'
			context = {"message": message}
			return render(request, 'login.html', context)

# 当前用户信息
@method_decorator(auth_login_required, name='dispatch')
class MyAccountView(View):
	def get(self, request):
		username = request.session.get('username')
		user_info = User.objects.get(username=username)
		context = {'user_info': user_info}
		return render(request, 'my_account.html', context)


# 修改密码
@method_decorator(auth_login_required, name='dispatch')
class PasswordChangeView(View):
	def get(self, request):
		username = request.GET.get('username')
		context = {'username': username}
		return render(request, 'password_change.html', context)

	def post(self, request):
		username = request.POST.get('username')
		old_password = request.POST.get('old_password')
		new_password = request.POST.get('new_password')
		confirm_new_password = request.POST.get('confirm_new_password')
		if new_password != confirm_new_password:
			message = 'confirm_new_password is not match'
			context = {"message": message, "username": username}
			return render(request, 'password_change.html', context)
		user = User.objects.filter(username=username).first()
		if check_password(old_password, user.password):
			user_for_update = User.objects.filter(username=username)
			user_for_update.update(password=make_password(new_password, None, 'pbkdf2_sha256'))
			message = 'Password Changed Successfully'
			context = {"message": message, "username": username}
			return render(request, 'password_change.html', context)
		else:
			message = 'Old password is wrong'
			context = {"message": message, "username": username}
			return render(request, 'password_change.html', context)

# 重置密码，管理员功能
@method_decorator(auth_login_required, name='dispatch')
class PasswordResetView(View):
	def get(self, request):
		username = request.GET.get('username')
		context = {'username': username}
		return render(request, 'password_reset.html', context)

	def post(self, request):
		username = request.POST.get('username')
		new_password = request.POST.get('new_password')
		confirm_new_password = request.POST.get('confirm_new_password')
		if new_password != confirm_new_password:
			message = 'confirm_new_password is not match'
			context = {"message": message, "username": username}
			return render(request, 'password_reset.html', context)
		else:
			user = User.objects.filter(username=username)
			user.update(password=make_password(new_password, None, 'pbkdf2_sha256'))
			message = 'Password Reseted Successfully'
			context = {"message": message, "username": username}
			return render(request, 'password_reset.html', context)

# 用户退出
class LogoutView(View):
	def get(self, request):
		request.session.flush()
		return redirect("/account/login")

# 用户列表
class UserListView(View):
	def get(self, request):
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		if filter_keyword != None:
			if filter_select == 'User Name =':
				user_lists = User.objects.filter(username=filter_keyword).order_by("username")
			if filter_select == 'Email':
				user_lists = User.objects.filter(email__icontains=filter_keyword).order_by("username")
			if filter_select == 'Superuser':
				user_lists = User.objects.filter(is_superuser=filter_keyword).order_by("username")
			if filter_select == 'Description':
				user_lists = User.objects.filter(description__icontains=filter_keyword).order_by("username")
			page_prefix = '?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword + '&page='
		else:
			user_lists = User.objects.all().order_by("username")
			page_prefix = '?page='
		page_num = request.GET.get('page')
		user_list = paginator_for_list_view(user_lists, page_num)
		curent_page_size = len(user_list)
		if filter_keyword == None:
			filter_keyword = ''
		if filter_select == None:
			filter_select = ''
		context = {
			'user_list': user_list, 
			'curent_page_size': curent_page_size, 
			'page_prefix': page_prefix, 
			'filter_keyword': filter_keyword, 
			'filter_select': filter_select
			}
		return render(request, 'user_list.html', context)

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/account/user_list?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# 创建用户
@method_decorator(auth_login_required, name='dispatch')
class UserCreateView(View):
	def get(self, request):
		return render(request, 'user_create.html')

	def post(self, request):
		username = request.POST.get('username')
		email = request.POST.get('email')
		role = request.POST.get('role')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		description = request.POST.get('description')
		if password != confirm_password:
			message = 'confirm_password is not match'
			context = {"message": message}
			return render(request, 'user_create.html', context)
		try:
			password=make_password(password, None, 'pbkdf2_sha256')
			User.objects.create(
				username=username, 
				email=email, 
				role=role, 
				password=password, 
				description=description
				)
			message = 'User [ ' + username + ' ] Successfully Created'
			context = {"message": message}
		except Exception as e:
			logging.error(e)
			message = "Failed to create user [ " + username + " ]"
			context = {"message": message}
		return render(request, 'user_create.html', context)

# 删除用户
@method_decorator(auth_login_required, name='dispatch')
class UserDeleteView(View):
	def get(self, request):
		username = request.GET.get('username')
		User.objects.filter(username=username).delete()
		return redirect('/account/user_list')
