from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import docker, logging, os, configparser, json

from ..models.docker_server_models import  Docker_Server

from ..utils.common_func import format_log, auth_controller, get_dir_info, get_file_contents, log_record


# 获取docker服务器及容器列表
@auth_controller
def docker_server(request):
	servers = Docker_Server.objects.all().order_by('ip')
	container_list = []
	for server in servers:
		containers = server.get_all_container_info()
		for container in containers:
			container_list.append(container)
	container_count = len(container_list)
	return render(request, 'docker_server.html', {'container_list': container_list, 'container_count': container_count})


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
