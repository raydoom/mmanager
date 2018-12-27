from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from dwebsocket import require_websocket, accept_websocket

import logging, os, json, time, threading

from ..models.server import Server, ServerType
from ..models.container import Container

from ..utils.common_func import format_log, auth_controller, get_dir_info, get_file_contents, log_record, get_time_stamp, send_data_over_websocket, shell_output_sender, shell_input_reciever
from ..utils.get_application_list import get_container_list

# 获取docker服务器及容器列表，根据选项和关键字过滤
@method_decorator(auth_controller, name='dispatch')
class Docker_Server_List(View):
	def get(self, request):
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		servers = ServerType.objects.get(server_type='docker').server_set.all().order_by('ip')
		container_list = []
		try:
			containers = get_container_list(servers)
			if filter_keyword != None:
				for container in containers:
					if filter_select == 'Status =' and filter_keyword.lower() == container.statename.lower():
						container_list.append(container)
					if filter_select == 'Name' and filter_keyword in container.name:
						container_list.append(container)		
					if filter_select == 'Location' and filter_keyword in container.host_ip:
						container_list.append(container)
			else:
				container_list = containers
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

# 实时查看容器日志
@auth_controller
@accept_websocket
def tail_container_log(request):
	if not request.is_websocket():
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		container_id = request.GET.get('container_id')
		container_name = request.GET.get('container_name')
		return render(request, 'tail_log.html', {'name': container_name, 'server_ip': server_ip})
	else: 
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		container_id = request.GET.get('container_id')
		container_name = request.GET.get('container_name')
		server = ServerType.objects.get(server_type='docker').server_set.all().get(ip=server_ip, port=int(server_port))
		container = Container()
		container.host_ip = server.ip
		container.host_port = server.port
		container.host_username = server.username
		container.host_password = server.password
		container.container_id = container_id
		channel = container.tail_container_logs()
		# 为每个websocket连接开启独立线程
		t = threading.Thread(target=send_data_over_websocket, args=(request,channel))
		t.start()
		t.join()

# 容器命令行实现
@auth_controller
@accept_websocket
def container_console(request):
	if not request.is_websocket():
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		container_id = request.GET.get('container_id')
		container_name = request.GET.get('container_name')
		return render(request, 'container_console.html', {'name': container_name, 'server_ip': server_ip})
	else:
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		container_id = request.GET.get('container_id')
		container_name = request.GET.get('container_name')
		server = ServerType.objects.get(server_type='docker').server_set.all().get(ip=server_ip, port=int(server_port))
		container = Container()
		container.host_ip = server.ip
		container.host_port = server.port
		container.host_username = server.username
		container.host_password = server.password
		container.container_id = container_id
		init_cmd = 'docker exec -it ' + container_id + ' bash\n'
		channel = container.container_shell()
		channel.send(init_cmd)
		time.sleep(1)
		channel.recv(16371)
		channel.send('\n')
		# th_reciever为接收用户输入线程 
		# th_sender为将shell输出发送到web端线程
		th_sender = threading.Thread(target=shell_output_sender, args=(request,channel))
		th_sender.start()
		th_reciever = threading.Thread(target=shell_input_reciever, args=(request,channel))
		th_reciever.start()
		th_sender.join()
		th_reciever.join()







