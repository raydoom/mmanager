from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
import xmlrpc.client, logging, os, configparser, json, time
from dwebsocket import require_websocket, accept_websocket

from ..models.server import Server, ServerType
from ..models.process import Process
from ..utils.common_func import get_time_stamp, format_log, auth_controller, log_record


# 获取supervisor服务器及程序列表，根据选项和关键字过滤
@method_decorator(auth_controller, name='dispatch')
class Supervisor_Server_List(View):
	def get(self, request):
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		servers = ServerType.objects.get(server_type='supervisor').server_set.all().order_by('ip')
		app_list = []
		for server in servers:
			try:
				apps = server.get_process_list()
				if filter_keyword != None:
					for app in apps:
						if filter_select == 'Status =' and filter_keyword.lower() == app['statename'].lower():
								app_list.append(app)
						if filter_select == 'App' and filter_keyword in app['name']:
								app_list.append(app)		
						if filter_select == 'Location' and filter_keyword in app['host_ip']:
								app_list.append(app)
				else:
					for app in apps:
						app_list.append(app)
			except Exception as e:
				logging.error(e)		
		app_count = len(app_list)
		return render(request, 'supervisor_server.html', {'app_list': app_list, 'app_count': app_count})

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/supervisorserver/?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# supervisor程序操作启动，停止，重启
@method_decorator(auth_controller, name='dispatch')
class process_option(View):
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


# # 获取supervisor程序的日志
# @method_decorator(auth_controller, name='dispatch')
# class Tail_process_name_Log(View):
# 	def get(self, request):
# 		server_ip = request.GET.get('server_ip')
# 		server_port = int(request.GET.get('server_port'))
# 		process_name = request.GET.get('process_name')
# 		server = Supervisor_Server.objects.filter(ip=server_ip).first()
# 		log = server.tail_process_name_log(process_name, format_log)
# 		return StreamingHttpResponse(log) # 使用StreamingHttpResponse返回yield对象，实现实时浏览日志

# 获取supervisor程序的日志
@auth_controller
@accept_websocket
def tail_process_log(request):
	global channel
	if not request.is_websocket():
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		process_name = request.GET.get('process_name')
		server = ServerType.objects.get(server_type='supervisor').server_set.all().get(ip=server_ip, port=int(server_port))
		process = Process()
		process.host_ip = server.ip
		process._host_port = server.port
		process.host_username = server.username
		process.host_password = server.password
		process.process_name = process_name		
		channel = process.tail_process_logs()
		wsurl = 'ws://' + request.get_host() + request.path

		return render(request, 'tail_log.html', {'wsurl': wsurl, 'name': process_name, 'server_ip': server_ip})
	else:
		while True:
			try:
				print (get_time_stamp(),request.websocket.is_closed())
				if request.websocket.is_closed(): #检测客户端心跳，如果客户端关闭，则停止读取和发送日志
					print ('websocket is closed')
					channel.close()
					break
				if channel.recv_ready():
					recvfromssh = channel.recv(16371)
					log = recvfromssh.decode()
					request.websocket.send(str(log))
				time.sleep(0.5)

			except Exception as e:
				logging.error(e)








			