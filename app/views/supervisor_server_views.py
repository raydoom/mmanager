# coding=utf8

from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
import logging, json, time, threading
from dwebsocket import require_websocket, accept_websocket

from ..models.server import Server, ServerType
from ..models.process import Process
from ..utils.common_func import get_time_stamp, format_log, auth_controller, log_record, send_data_over_websocket
from ..utils.get_application_list import get_process_lists


# 获取supervisor服务器及程序列表，根据选项和关键字过滤
@method_decorator(auth_controller, name='dispatch')
class Supervisor_Server_List(View):
	def get(self, request):
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		servers = ServerType.objects.get(server_type='supervisor').server_set.all().order_by('ip')
		process_list = []
		try:
			processes = get_process_lists(servers)
			if filter_keyword != None:
				for process in processes:
					if filter_select == 'Status =' and filter_keyword.lower() == process.statename.lower():
							process_list.append(process)
					if filter_select == 'Name' and filter_keyword in process.name:
							process_list.append(process)		
					if filter_select == 'Location' and filter_keyword in process.host_ip:
							process_list.append(process)
			else:
				process_list = processes
		except Exception as e:
			logging.error(e)		
		process_count = len(process_list)
		if filter_keyword == None:
			filter_keyword = ''
		if filter_select == None:
			filter_select = ''
		return render(request, 'supervisor_server.html', {'process_list': process_list, 'process_count': process_count, 'filter_keyword': filter_keyword, 'filter_select': filter_select})

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/supervisorserver/?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# supervisor程序操作启动，停止，重启
@method_decorator(auth_controller, name='dispatch')
class Process_Option(View):
	def get(self, request):
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		process_name = request.GET.get('process_name')
		process_opt = request.GET.get('process_opt')
		server = ServerType.objects.get(server_type='supervisor').server_set.all().get(ip=server_ip, port=int(server_port))
		process = Process()
		process.host_ip = server.ip
		process._host_port = server.port
		process.host_username = server.username
		process.host_password = server.password
		process.name = process_name		
		result = process.process_opt(process_opt)
		log_detail = process_opt + ' <' + process_name + '> on host ' + server_ip
		log_record(request.session.get('username'), log_detail=log_detail)
		return HttpResponse(result)

# 获取supervisor程序的日志
@auth_controller
@accept_websocket
def tail_process_log(request):
	if not request.is_websocket():
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		process_name = request.GET.get('process_name')
		return render(request, 'tail_log.html', {'name': process_name, 'server_ip': server_ip})
	else:
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		process_name = request.GET.get('process_name')
		server = ServerType.objects.get(server_type='supervisor').server_set.all().get(ip=server_ip, port=int(server_port))
		process = Process()
		process.host_ip = server.ip
		process.host_port = server.port
		process.host_username = server.username
		process.host_password = server.password
		process.process_name = process_name		
		channel = process.tail_process_logs()
		# 为每个websocket连接开启独立线程
		t = threading.Thread(target=send_data_over_websocket, args=(request,channel))
		t.start()
		t.join()








			