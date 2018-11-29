from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import docker, logging, os, configparser, json

from ..models.docker_server_models import  Docker_Server

from ..utils.common_func import format_log, auth_controller, get_dir_info, get_file_contents, log_record


# 获取docker服务器及容器列表，根据选项和关键字过滤
@method_decorator(auth_controller, name='dispatch')
class Docker_Server_List(View):
	def get(self, request):
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		servers = Docker_Server.objects.all().order_by('ip')
		container_list = []
		for server in servers:
			containers = server.get_all_container_info()
			if filter_keyword != None:
				for container in containers:
					if filter_select == 'Status =' and filter_keyword.lower() == container.status.lower():
							container_list.append(container)
					if filter_select == 'App' and filter_keyword in container.name:
							container_list.append(container)		
					if filter_select == 'Location' and filter_keyword in container.host_ip:
							container_list.append(container)
			else:
				for container in containers:
					container_list.append(container)
		container_count = len(container_list)
		return render(request, 'docker_server.html', {'container_list': container_list, 'container_count': container_count})

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/dockerserver/?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# 容器操作启动，停止，重启
@method_decorator(auth_controller, name='dispatch')
class Container_Option(View):
	def get(self, request):
		print (request.get_full_path() )
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		container_id = request.GET.get('container_id')
		container_name = request.GET.get('container_name')
		container_opt = request.GET.get('container_opt')
		server = Docker_Server.objects.filter(ip=server_ip).first()
		result = server.container_opt(container_id, container_opt)
		log_detail = container_opt + ' <' + container_name + '> on host ' + server_ip
		log_record(request.session.get('username'), log_detail=log_detail)
		return redirect('/dockerservers/')

# 获取容器日志
@method_decorator(auth_controller, name='dispatch')
class Tail_Container_Log(View):
	def get(self, request):
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		container_id = request.GET.get('container_id')	
		server = Docker_Server.objects.filter(ip=server_ip).first()
		log = server.tail_container_log(container_id, format_log)
		return StreamingHttpResponse(log)
		#return render(request, 'tail.html', {'log': log})