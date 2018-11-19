from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse  
from django.contrib.auth import models, authenticate
# from django.contrib.auth.decorators import login_required

import docker, xmlrpc.client, logging, os, configparser
from .models import Supervisor_Server, Docker_Server
from .common_func import format_log, auth_controller, get_dir_info, get_file_contents
from django.conf import settings
from .models import User_Log

# 获取cconfig.ini中的配置项
CONF_DIRS=(settings.BASE_DIR+'/config')
conf_dir = configparser.ConfigParser()
conf_dir.read(CONF_DIRS+'/config.ini')

dir_root = conf_dir.get('dir_info', 'dir_root')
offset = int(conf_dir.get('dir_info', 'offset'))

# 获取docker服务器及容器列表
@auth_controller
def docker_server(request):
	print (request.GET.get('REMOTE_ADDR'))
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
	log_user=request.session.get('username')
	log_detail=log_user + ' ' + container_opt + ' ' + container_id + ' on host ' + server_ip
	log_record(log_user=log_user, log_detail=log_detail)
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
	log_user=request.session.get('username')
	log_detail=log_user + ' ' + supervisor_opt + ' ' + supervisor_app + ' on host' + server_ip
	log_record(log_user=log_user, log_detail=log_detail)
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


# 本地日志目录浏览
def dir_viewer(request):
	current_dir = ''
	to_dir_name = ''
	to_dir = dir_root
	if request.GET.get('current_dir'):
		current_dir = request.GET.get('current_dir')
	if request.GET.get('to_dir_name'):
		to_dir_name = request.GET.get('to_dir_name')
		if to_dir_name == '..':
			list_c =  current_dir.split('/')
			#to_dir = list_c[1] + '/'
			to_dir = ''
			for i in range(0,len(list_c)-2):
				to_dir = to_dir + list_c[i] + '/'
			print (to_dir)
			current_dir = to_dir
			to_dir = dir_root + '/' + to_dir
			
			dir_infos = get_dir_info(to_dir)
			return render(request, 'dir_viewer.html', {'dir_infos': dir_infos, 'current_dir': current_dir})
		else:
			to_dir = dir_root + current_dir + to_dir_name + '/'
	dir_infos = get_dir_info(to_dir)
	return render(request, 'dir_viewer.html', {'dir_infos': dir_infos, 'current_dir': current_dir + to_dir_name + '/'})

# 本地日志文件浏览
def text_viewer(request):
	current_dir = dir_root
	if request.GET.get('current_dir'):
		current_dir = dir_root + request.GET.get('current_dir')
	file_name = request.GET.get('file_name')
	text_contents = []
	text_contents = get_file_contents(current_dir, file_name, offset)
	return render(request, 'text_viewer.html', {'text_contents': text_contents})


# 记录日志函数
def log_record(log_user, log_detail):
	return (User_Log.objects.create(log_user=log_user, log_detail=log_detail))

# 操作日志查看页面试图函数
def actions_log(request):
	actions_log = User_Log.objects.all().order_by('-log_time')
	return render(request, 'actions_log.html', {'actions_log': actions_log})

# 文件下载视图函数
def file_download(request):  
	current_dir = request.GET.get('current_dir')
	to_dir_name = request.GET.get('to_dir_name')
	filename = dir_root + current_dir + to_dir_name
	file=open(filename, 'rb')  
	response =FileResponse(file)
	response['Content-Type']='application/octet-stream'
	Content_Disposition = 'attachment;filename=' + to_dir_name
	response['Content-Disposition']=Content_Disposition
	return response 
