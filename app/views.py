from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from django.contrib.auth import models, authenticate
# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import docker, xmlrpc.client, logging, os, configparser, json

from .models.docker_server import  Docker_Server
from .models.supervisor_server import Supervisor_Server
from .models.jenkins_server import Jenkins_Server
from .models.user_log import User_Log

from .common_func import format_log, auth_controller, get_dir_info, get_file_contents, log_record
from django.conf import settings


# 获取cconfig.ini中的配置项
CONF_DIRS=(settings.BASE_DIR+'/config')
conf_dir = configparser.ConfigParser()
conf_dir.read(CONF_DIRS+'/config.ini')

dir_root = conf_dir.get('dir_info', 'dir_root')
lines_per_page = int(conf_dir.get('dir_info', 'lines_per_page'))

# 获取docker服务器及容器列表
@auth_controller
def docker_server(request):
	servers = Docker_Server.objects.all().order_by('ip')
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
	container_name = request.GET.get('container_name')
	container_opt = request.GET.get('container_opt')
	server = Docker_Server.objects.filter(ip=server_ip).first()
	result = server.container_opt(container_id, container_opt)
	log_user=request.session.get('username')
	log_detail=log_user + ' ' + container_opt + ' <' + container_name + '> on host ' + server_ip
	log_record(log_user=log_user, log_detail=log_detail)
	return redirect('/dockerservers/')


# 获取容器日志
@auth_controller
def tail_container_log(request):
	server_ip = request.GET.get('server_ip')
	server_port = int(request.GET.get('server_port'))
	container_id = request.GET.get('container_id')	
	server = Docker_Server.objects.filter(ip=server_ip).first()
	log = server.tail_container_log(container_id, format_log)
	return StreamingHttpResponse(log)
	#return render(request, 'tail.html', {'log': log})


# 获取supervisor服务器及程序列表
@auth_controller
def supervisor_server(request):
	servers = Supervisor_Server.objects.all().order_by('ip')
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
	server = Supervisor_Server.objects.filter(ip=server_ip).first()
	result = server.supervisor_app_opt(supervisor_app, supervisor_opt)
	log_user=request.session.get('username')
	log_detail=log_user + ' ' + supervisor_opt + ' <' + supervisor_app + '> on host ' + server_ip
	log_record(log_user=log_user, log_detail=log_detail)
	return redirect('/dockerservers/')


# 获取supervisor程序的日志
@auth_controller
def tail_supervisor_app_log(request):
	server_ip = request.GET.get('server_ip')
	server_port = int(request.GET.get('server_port'))
	supervisor_app = request.GET.get('supervisor_app')
	server = Supervisor_Server.objects.filter(ip=server_ip).first()
	log = server.tail_supervisor_app_log(supervisor_app, format_log)
	return StreamingHttpResponse(log) # 使用StreamingHttpResponse返回yield对象，实现实时浏览日志

# jenkins任务列表视图
@auth_controller
def jenkins_server(request):
	servers = Jenkins_Server.objects.all().order_by('ip')
	server_all_list = []
	for server in servers:
		server_jobs_dict = {}
		server_jobs_dict['ip'] = server.ip
		server_jobs_dict['port'] = server.port
		jobs = server.get_all_jobs_list()
		server_jobs_dict['jobs'] = jobs
		server_all_list.append(server_jobs_dict)
	return render(request, 'jenkins_server.html', {'server_all_list': server_all_list})


# jenkins操作
@auth_controller
def jenkins_job_opt(request):
	server_ip = request.GET.get('server_ip')
	server_port = int(request.GET.get('server_port'))
	job_name = request.GET.get('job_name')
	jenkins_opt = request.GET.get('jenkins_opt')
	server = Jenkins_Server.objects.filter(ip=server_ip).first()
	result = server.send_build_job(job_name)
	log_user=request.session.get('username')
	log_detail=log_user + ' ' + jenkins_opt + ' ' + job_name + ' on host ' + server_ip
	log_record(log_user=log_user, log_detail=log_detail)
	return redirect('/jenkinsservers/')


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
	text_contents = get_file_contents(dist, lines_per_page)
	log_user=request.session.get('username')
	log_detail=log_user + ' viewer ' + dist
	log_record(log_user=log_user, log_detail=log_detail)
	return render(request, 'text_viewer.html', {'text_contents': text_contents})


# 记录日志函数
# def log_record(log_user, log_detail):
# 	return (User_Log.objects.create(log_user=log_user, log_detail=log_detail))


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


 	
