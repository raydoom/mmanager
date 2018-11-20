from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse  
from django.contrib.auth import models, authenticate
# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


## 本地日志目录浏览
def dir_viewer(request):
	dist = '/'
	current_dir = '/'
	if request.GET.get('dist'):
		dist = request.GET.get('dist') + '/'
		if dist.split('/')[-2] == '..': 
			dist_list = dist.split('/')
			dist = ''
			for i in range(0,len(dist_list)-3):
				dist = dist + dist_list[i] +'/'
	current_dir = dist			
	dist = dir_root + dist	
	dir_infos = get_dir_info(dist)
	return render(request, 'dir_viewer.html', {'dir_infos': dir_infos, 'current_dir': current_dir})


# 本地日志文件浏览
def text_viewer(request):
	dist = dir_root
	if request.GET.get('dist'):
		dist = request.GET.get('dist')
		dist = dir_root + dist
	text_contents = []
	text_contents = get_file_contents(dist, offset)
	log_user=request.session.get('username')
	log_detail=log_user + ' viewer ' + dist
	log_record(log_user=log_user, log_detail=log_detail)
	return render(request, 'text_viewer.html', {'text_contents': text_contents})


# 记录日志函数
def log_record(log_user, log_detail):
	return (User_Log.objects.create(log_user=log_user, log_detail=log_detail))


# 操作日志查看页面试图函数
def actions_log(request):
	actions_logs = User_Log.objects.all().order_by('-log_time')
	paginator = Paginator(actions_logs, 10)
	page = request.GET.get('page')
	try:
		actions_log = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		actions_log = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		actions_log = paginator.page(paginator.num_pages)
	return render(request, 'actions_log.html', {'actions_log': actions_log})


# 文件下载视图函数
def file_download(request):  
	filepath = request.GET.get('filepath')
	filepath = dir_root + filepath
	file=open(filepath, 'rb')  
	response =FileResponse(file)
	response['Content-Type']='application/octet-stream'
	filename = filepath.split('/')[-1]
	Content_Disposition = 'attachment;filename=' + filename
	response['Content-Disposition']=Content_Disposition
	return response 
