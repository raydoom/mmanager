from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dwebsocket import require_websocket, accept_websocket

import docker, logging, os, configparser, json, time

from ..models.server import Server, ServerType
from ..models.container import Container

from ..utils.common_func import format_log, auth_controller, get_dir_info, get_file_contents, log_record, get_time_stamp


# 获取docker服务器及容器列表，根据选项和关键字过滤
@method_decorator(auth_controller, name='dispatch')
class Docker_Server_List(View):
	def get(self, request):
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		servers = ServerType.objects.get(server_type='docker').server_set.all().order_by('ip')
		container_list = []
		for server in servers:
			try:
				containers = server.get_container_list()
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
		server = ServerType.objects.get(server_type='docker').server_set.all().get(ip=server_ip, port=int(server_port))
		container = Container()
		container.host_ip = server.ip
		container._host_port = server.port
		container.host_username = server.username
		container.host_password = server.password
		container.container_id = container_id
		result = container.container_opt(container_opt)
		log_detail = container_opt + ' <' + container_name + '> on host ' + server_ip
		log_record(request.session.get('username'), log_detail=log_detail)
		return HttpResponse(result)

# 获取容器日志
@auth_controller
@accept_websocket
def tail_container_log(request):
	global channel
	if not request.is_websocket():
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		container_id = request.GET.get('container_id')
		container_name = request.GET.get('container_name')
		server = ServerType.objects.get(server_type='docker').server_set.all().get(ip=server_ip, port=int(server_port))
		container = Container()
		container.host_ip = server.ip
		container._host_port = server.port
		container.host_username = server.username
		container.host_password = server.password
		container.container_id = container_id
		channel = container.tail_container_logs()
		wsurl = 'ws://' + request.get_host() + request.path

		return render(request, 'tail_log.html', {'wsurl': wsurl, 'name': container_name, 'server_ip': server_ip})
	else:
		while True:
			try:
				if request.websocket.is_closed(): #检测客户端心跳，如果客户端关闭，则停止读取和发送日志
					print ('websocket is closed')
					channel.close()
					break
				if channel.recv_ready():
					recvfromssh = channel.recv(16371)
					log = recvfromssh.decode()
					request.websocket.send(log)
				time.sleep(0.5)
			except Exception as e:
				logging.error(e)

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
		container_name = request.GET.get('container_name')	
		wsurl = 'ws://' + request.get_host() + request.path
		server_cmd = Docker_Server.objects.filter(ip=server_ip).first()
		return render(request, 'container_console.html', {'wsurl': wsurl, 'name': container_name, 'server_ip': server_ip})
	else:
		for cmd in request.websocket:
			cmd = cmd.decode()
			print (cmd)
			result = server_cmd.exec_cmd(container_id, cmd)[1].decode()
			request.websocket.send(str(result))







