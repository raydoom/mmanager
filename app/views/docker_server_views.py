from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dwebsocket import require_websocket, accept_websocket

import docker, logging, os, configparser, json, time

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
			try:
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
			except Exception as e:
				logging.error(e)
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
		return HttpResponse(result)

# # 获取容器日志
# @method_decorator(auth_controller, name='dispatch')
# class Tail_Container_Log(View):
# 	@accept_websocket
# 	def get(self, request):
# 		server_ip = request.GET.get('server_ip')
# 		server_port = int(request.GET.get('server_port'))
# 		container_id = request.GET.get('container_id')	
# 		server = Docker_Server.objects.filter(ip=server_ip).first()
# 		log = server.tail_container_log(container_id)
# 		return StreamingHttpResponse(log)
# 		#return render(request, 'tail.html', {'log': log})

# 获取容器日志
@auth_controller
@accept_websocket
def tail_container_log(request):
	global log_generator
	if not request.is_websocket():
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		container_id = request.GET.get('container_id')	
		wsurl = request.get_host()+request.path
		server = Docker_Server.objects.filter(ip=server_ip).first()
		log_generator = server.tail_container_logs(container_id)
		return render(request, 'tail_log.html', {'wsurl': wsurl, 'container_id': container_id, 'server_ip': server_ip})
	else:
		for log in log_generator:
			print (log)
			request.websocket.send(log)

# 容器命令行
@auth_controller
@accept_websocket
def container_console(request):
	global container_id
	global server_cmd
	if not request.is_websocket():
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		container_id = request.GET.get('container_id')	
		wsurl = request.get_host()+request.path
		server_cmd = Docker_Server.objects.filter(ip=server_ip).first()
		return render(request, 'container_console.html', {'wsurl': wsurl, 'container_id': container_id, 'server_ip': server_ip})
	else:
		for cmd in request.websocket:
			cmd = cmd.decode()
			print (cmd)
			result = server_cmd.exec_cmd(container_id, cmd)[1].decode()
			request.websocket.send(str(result))







