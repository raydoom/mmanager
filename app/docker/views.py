# coding=utf8

import logging
import threading
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from dwebsocket import require_websocket
from dwebsocket import accept_websocket

from app.server.models import Server
from app.server.models import ServerType
from app.docker.container import Container
from app.docker.models import ContainerInfoCache
from app.utils.common_func import auth_login_required
from app.utils.common_func import log_record
from app.utils.common_func import send_data_over_websocket
from app.utils.common_func import shell_output_sender
from app.utils.common_func import shell_input_reciever
from app.utils.get_application_list import get_container_lists
from app.utils.paginator import paginator_for_list_view

# 获取docker服务器及容器列表，根据选项和关键字过滤
@method_decorator(auth_login_required, name='dispatch')
class ContainerListView(View):
	def get(self, request):
		current_user_id = request.session.get('user_id')
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		try:
			server_type_id = ServerType.objects.filter(server_type='docker').first().server_type_id
			servers = Server.objects.filter(server_type_id=server_type_id).order_by('host')
		except Exception as e:
			logging.error(e)
			servers = []
		container_list = []
		try:
			containers = get_container_lists(servers)
			for container in containers:
				container_info = ContainerInfoCache(
					host=container.host,
					host_port=container.host_port,
					container_id=container.container_id,
					image=container.image,
					command=container.command,
					created=container.created,
					statename=container.statename,
					status=container.status,
					port=container.port,
					name=container.name,
					current_user_id=current_user_id
					)
				container_list.append(container_info)
			ContainerInfoCache.objects.filter(current_user_id=current_user_id).delete()
			ContainerInfoCache.objects.bulk_create(container_list)
		except Exception as e:
			logging.error(e)
		if filter_keyword != None:
			if filter_select == 'Status =':
				container_lists = ContainerInfoCache.objects.filter(
					current_user_id=current_user_id,
					status=filter_keyword
					)
			if filter_select == 'Name':
				container_lists = ContainerInfoCache.objects.filter(
					current_user_id=current_user_id,
					name__icontains=filter_keyword
					)
			if filter_select == 'Host':
				container_lists = ContainerInfoCache.objects.filter(
					current_user_id=current_user_id,
					host__icontains=filter_keyword
					)
			page_prefix = '?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword + '&page='
		else:
			container_lists = ContainerInfoCache.objects.filter(current_user_id=current_user_id)
			page_prefix = '?page='
		page_num = request.GET.get('page')
		container_list = paginator_for_list_view(container_lists, page_num)
		curent_page_size = len(container_list)
		if filter_keyword == None:
			filter_select = ''
			filter_keyword = ''
		context = {
			'container_list': container_list, 
			'curent_page_size':curent_page_size, 
			'filter_keyword': filter_keyword, 
			'filter_select': filter_select, 
			'page_prefix': page_prefix
			}
		return render(request, 'container_list.html', context)
		
	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/docker/container_list?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# 容器操作启动，停止，重启
@method_decorator(auth_login_required, name='dispatch')
class ContainerOptionView(View):
	def get(self, request):
		host = request.GET.get('host')
		host_port = int(request.GET.get('host_port'))
		container_id = request.GET.get('container_id')
		container_name = request.GET.get('container_name')
		container_opt = request.GET.get('container_opt')
		server_type_id = ServerType.objects.get(server_type='docker').server_type_id
		server = Server.objects.get(server_type_id=server_type_id, host=host, port=host_port)
		container = Container()
		container.host = server.host
		container.host_port = server.port
		container.host_username = server.username
		container.host_password = server.password
		container.container_id = container_id
		result = container.container_opt(container_opt)
		log_detail = container_opt + ' <' + container_name + '> on host ' + host
		log_record(request.session.get('username'), log_detail=log_detail)
		return HttpResponse(result)

# 实时查看容器日志
@auth_login_required
@accept_websocket
def container_log(request):
	if not request.is_websocket():
		host = request.GET.get('host')
		host_port = int(request.GET.get('host_port'))
		container_id = request.GET.get('container_id')
		container_name = request.GET.get('container_name')
		context = {'name': container_name, 'host': host}
		return render(request, 'tail_log.html', context)
	else: 
		host = request.GET.get('host')
		host_port = int(request.GET.get('host_port'))
		container_id = request.GET.get('container_id')
		container_name = request.GET.get('container_name')
		server_type_id = ServerType.objects.get(server_type='docker').server_type_id
		server = Server.objects.get(server_type_id=server_type_id, host=host, port=host_port)
		container = Container()
		container.host = server.host
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
@auth_login_required
@accept_websocket
def container_console(request):
	if not request.is_websocket():
		host = request.GET.get('host')
		host_port = int(request.GET.get('host_port'))
		container_id = request.GET.get('container_id')
		container_name = request.GET.get('container_name')
		context= {'name': container_name, 'host': host}
		return render(request, 'container_console.html', context)
	else:
		host = request.GET.get('host')
		host_port = int(request.GET.get('host_port'))
		container_id = request.GET.get('container_id')
		container_name = request.GET.get('container_name')
		server_type_id = ServerType.objects.get(server_type='docker').server_type_id
		server = Server.objects.get(server_type_id=server_type_id, host=host, port=host_port)
		container = Container()
		container.host = server.host
		container.host_port = server.port
		container.host_username = server.username
		container.host_password = server.password
		container.container_id = container_id
		channel = container.container_shell()
		init_cmd = 'docker exec -it ' + container_id + ' bash\n'
		channel.send(init_cmd)
		time.sleep(1)
		init_recieve = channel.recv(16371).decode()
		# 不支持bash的容器，用sh进行连接
		if 'executable file not found' in init_recieve:
			init_cmd = 'docker exec -it ' + container_id + ' sh\n'
			channel.send(init_cmd)
			time.sleep(1)
			init_recieve = channel.recv(16371).decode()
		# 连接错误，返回
		if 'Error' in init_recieve:
			logging.error(init_recieve)
			request.websocket.send(' container is not running or not support shell... ')
			time.sleep(60)
			return 0
		channel.send('\n')
		# th_reciever为接收用户输入线程 
		# th_sender为将shell输出发送到web端线程
		th_sender = threading.Thread(target=shell_output_sender, args=(request,channel))
		th_sender.start()
		th_reciever = threading.Thread(target=shell_input_reciever, args=(request,channel))
		th_reciever.start()
		th_sender.join()
		th_reciever.join()







