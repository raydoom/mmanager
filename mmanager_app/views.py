from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import models, authenticate
# from django.contrib.auth.decorators import login_required

import docker, xmlrpc.client, logging
from .models import Supervisor_Server, Docker_Server
from .common_func import format_log, auth_controller

# 获取docker服务器及容器列表
@auth_controller
def docker_server(request):
	servers = Docker_Server.objects.all()
	server_all_list = []
	for server in servers:
		server_dict = {}
		server_dict['ip'] = server.ip
		server_dict['port'] = server.port
		server_dict['containers'] = server.get_all_container_info()
		server_all_list.append(server_dict)
	return render(request, 'docker_server.html', {'server_all_list': server_all_list})


# 容器操作启动，停止，重启
@auth_controller
def container_option(request):
	server_ip = request.GET.get('server_ip')
	server_port = int(request.GET.get('server_port'))
	container_id = request.GET.get('container_id')
	container_opt = request.GET.get('container_opt')
	servers = Docker_Server.objects.filter(ip=server_ip)
	for server in servers:
		result = server.container_opt(container_id, container_opt)
	print (result)
	return redirect('/docker_servers/')

# 获取容器日志
@auth_controller
def tail_container_log(request):
	server_ip = request.GET.get('server_ip')
	server_port = int(request.GET.get('server_port'))
	container_id = request.GET.get('container_id')	
	servers = Docker_Server.objects.filter(ip=server_ip)
	for server in servers:
		server = server
	log = server.tail_container_log(container_id)
	return render(request, 'tail.html', {'log': log})


# 获取supervisor服务器及程序列表
@auth_controller
def supervisor_server(request):
	servers = Supervisor_Server.objects.all()
	server_all_list = []
	for server in servers:
		server_app_dict = {}
		server_app_dict['ip'] = server.ip
		server_app_dict['port'] = server.port
		apps = server.get_all_process_info()
		server_app_dict['apps'] = apps
		server_all_list.append(server_app_dict)
	return render(request, 'supervisor_server.html', {'server_all_list': server_all_list})


# supervisor程序操作启动，停止，重启
@auth_controller
def supervisor_app_option(request):
	server_ip = request.GET.get('server_ip')
	server_port = int(request.GET.get('server_port'))
	supervisor_app = request.GET.get('supervisor_app')
	supervisor_opt = request.GET.get('supervisor_opt')
	servers = Supervisor_Server.objects.filter(ip=server_ip)
	for server in servers:
		result = server.supervisor_app_opt(supervisor_app, supervisor_opt)
	return redirect('/docker_servers/')

# 获取supervisor程序的日志
@auth_controller
def tail_supervisor_app_log(request):
	server_ip = request.GET.get('server_ip')
	server_port = int(request.GET.get('server_port'))
	supervisor_app = request.GET.get('supervisor_app')
	servers = Supervisor_Server.objects.filter(ip=server_ip)
	for server in servers:
		server = server
	log = server.tail_supervisor_app_log(supervisor_app)
	return render(request, 'tail.html', {'log': log})


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

# 用户退出
@auth_controller
def logout(request):
	request.session.flush()
	return redirect("/index/")

# 用户注册
def register(request):
	pass
	return redirect("/index/")
