# coding=utf8

from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from dwebsocket import require_websocket, accept_websocket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging, os, json, time, threading

from app.server.models import Server, ServerType
from app.docker.container import Container

from app.docker.models import ContainerInfo
from app.utils.common_func import format_log, auth_controller, get_dir_info, get_file_contents, log_record, get_time_stamp, send_data_over_websocket, shell_output_sender, shell_input_reciever
from app.utils.get_application_list import get_container_lists

# 获取docker服务器及容器列表，根据选项和关键字过滤
@method_decorator(auth_controller, name='dispatch')
class ContainerListView(View):
	def get(self, request):
		current_user_id = request.session.get('user_id')
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		servers = ServerType.objects.get(server_type='docker').server_set.all().order_by('ip')
		container_list = []
		try:
			containers = get_container_lists(servers)
			for container in containers:
				container_list.append(ContainerInfo(host_ip=container.host_ip,
															host_port=container.host_port,
															host_username=container.host_username,
															container_id=container.container_id,
															host_password=container.host_password,
															image=container.image,
															command=container.command,
															created=container.created,
															statename=container.statename,
															status=container.status,
															port=container.port,
															name=container.name,
															current_user_id=current_user_id))
			ContainerInfo.objects.filter(current_user_id=current_user_id).delete()
			ContainerInfo.objects.bulk_create(container_list)
		except Exception as e:
			logging.error(e)
		if filter_keyword != None:
			if filter_select == 'Status =':
				container_list = ContainerInfo.objects.filter(current_user_id=current_user_id,status=filter_keyword)
			if filter_select == 'Name':
				container_list = ContainerInfo.objects.filter(current_user_id=current_user_id,name__icontains=filter_keyword)
			if filter_select == 'Location':
				container_list = ContainerInfo.objects.filter(current_user_id=current_user_id,host_ip__icontains=filter_keyword)
			page_prefix = '?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword + '&page='
		else:
			container_list = ContainerInfo.objects.filter(current_user_id=current_user_id)
			page_prefix = '?page='
		paginator = Paginator(container_list, 10)
		page = request.GET.get('page')
		try:
			container_list = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			container_list = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			container_list = paginator.page(paginator.num_pages)
		container_count = len(container_list)
		if filter_keyword == None:
			filter_select = ''
			filter_keyword = ''
		return render(request, 'container_list.html', {'container_list': container_list, 'container_count': container_count, 'filter_keyword': filter_keyword, 'filter_select': filter_select, 'page_prefix': page_prefix})
	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/docker/container_list?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# 容器操作启动，停止，重启
@method_decorator(auth_controller, name='dispatch')
class ContainerOptionView(View):
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
def container_log(request):
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







