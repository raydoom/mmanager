from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth import models, authenticate
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
import logging, os, configparser, json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.user_info_models import User_Info, Role, Permission
from ..utils.common_func import auth_controller, log_record


# 用户登陆
class Login(View):
	def get(self, request):
		return render(request, 'login.html')

	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		# if authenticate(username=username, password=password):
		user = User_Info.objects.filter(username=username).first()
		if user:
			if check_password(password, user.password):
				request.session['islogin'] = True
				request.session['username'] = username
				request.session['is_superuser'] = user.is_superuser
				return redirect("/index/")
		else:
			message = 'username or password error!'
			return render(request, 'login.html', {"message": message})

# 当前用户信息
@method_decorator(auth_controller, name='dispatch')
class Account(View):
	def get(self, request):
		username = request.session.get('username')
		userinfo = User_Info.objects.get(username=username)
		return render(request, 'account.html', {'userinfo': userinfo})

# 添加用户
@method_decorator(auth_controller, name='dispatch')
class Add_User(View):
	def get(self, request):
		return render(request, 'account.html', {'userinfo': userinfo})

# 修改密码
@method_decorator(auth_controller, name='dispatch')
class Change_Password(View):
	def get(self, request):
		username = request.GET.get('username')
		return render(request, 'change_password.html', {'username': username})

	def post(self, request):
		username = request.POST.get('username')
		old_password = request.POST.get('old_password')
		new_password = request.POST.get('new_password')
		confirm_new_password = request.POST.get('confirm_new_password')
		if new_password != confirm_new_password:
			message = 'confirm_new_password is not match'
			return render(request, 'change_password.html', {"message": message, "username": username})

		user = User_Info.objects.filter(username=username).first()
		if check_password(old_password, user.password):
			User_Info.objects.filter(username=username).update(password=make_password(new_password, None, 'pbkdf2_sha256'))
		# if authenticate(username=username, password=old_password):
		# 	models.User.objects.filter(username=username).update(password=make_password(new_password, None, 'pbkdf2_sha256'))
			message = 'Password Successfully Changed'
			return render(request, 'change_password.html', {"message": message, "username": username})
		else:
			message = 'Old password is wrong'
			return render(request, 'change_password.html', {"message": message, "username": username})


# 用户退出
class Sign_Out(View):
	def get(self, request):
		request.session.flush()
		return redirect("/index/")


# 用户注册
class Register(View):
	def get(self, request):
		return redirect("/index/")

# 用户列表
class Users(View):
	def get(self, request):
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		if filter_keyword != None:
			if filter_select == 'User Name =':
				user_lists = User_Info.objects.filter(username=filter_keyword).order_by("username")
			if filter_select == 'Email':
				user_lists = User_Info.objects.filter(email__icontains=filter_keyword).order_by("username")
			if filter_select == 'Superuser':
				user_lists = User_Info.objects.filter(is_superuser=filter_keyword).order_by("username")
			if filter_select == 'Description':
				user_lists = User_Info.objects.filter(description__icontains=filter_keyword).order_by("username")
			page_prefix = '?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword + '&page='
		else:
			user_lists = User_Info.objects.all().order_by("username")
			page_prefix = '?page='
		paginator = Paginator(user_lists, 10)
		page = request.GET.get('page')
		try:
			user_list = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			user_list = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			user_list = paginator.page(paginator.num_pages)
		user_list_count = len(user_lists)
		return render(request, 'users.html', {'user_list': user_list, 'user_list_count': user_list_count, 'page_prefix': page_prefix})

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/users/?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# 修改密码
@method_decorator(auth_controller, name='dispatch')
class Create_User(View):
	def get(self, request):
		return render(request, 'create_user.html')

	def post(self, request):
		username = request.POST.get('username')
		email = request.POST.get('email')
		is_superuser = request.POST.get('is_superuser')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		description = request.POST.get('description')

		if password != confirm_password:
			message = 'confirm_password is not match'
			return render(request, 'create_user.html', {"message": message})
		try:
			password=make_password(password, None, 'pbkdf2_sha256')
			User_Info.objects.create(username=username, email=email, is_superuser=is_superuser, password=password, description=description)
			message = 'User [ ' + username + ' ] Successfully Created'
		except Exception as e:
			logging.error(e)
			message = "Failed to create user [ " + username + " ]"
		return render(request, 'create_user.html', {"message": message})
# 删除用户
@method_decorator(auth_controller, name='dispatch')
class Delete_User(View):
	def get(self, request):
		username = request.GET.get('username')
		User_Info.objects.filter(username=username).delete()
		return redirect('/users/')