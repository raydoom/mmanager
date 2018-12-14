from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
import xmlrpc.client, logging, os, configparser, json
from dwebsocket import require_websocket, accept_websocket

from ..models.supervisor_server_models import Supervisor_Server
from ..utils.common_func import get_time_stamp, format_log, auth_controller, log_record


# 获取supervisor服务器及程序列表，根据选项和关键字过滤
@method_decorator(auth_controller, name='dispatch')
class Supervisor_Server_List(View):
	def get(self, request):
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		servers = Supervisor_Server.objects.all().order_by('ip')
		app_list = []
		for server in servers:
			try:
				apps = server.get_all_process_info()
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
class Supervisor_App_Option(View):
	def get(self, request):
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		supervisor_app = request.GET.get('supervisor_app')
		supervisor_opt = request.GET.get('supervisor_opt')
		server = Supervisor_Server.objects.filter(ip=server_ip).first()
		result = server.supervisor_app_opt(supervisor_app, supervisor_opt)
		log_detail = supervisor_opt + ' <' + supervisor_app + '> on host ' + server_ip
		log_record(request.session.get('username'), log_detail=log_detail)
		return HttpResponse(result)


# 获取supervisor程序的日志
@method_decorator(auth_controller, name='dispatch')
class Tail_Supervisor_App_Log(View):
	def get(self, request):
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		supervisor_app = request.GET.get('supervisor_app')
		server = Supervisor_Server.objects.filter(ip=server_ip).first()
		log = server.tail_supervisor_app_log(supervisor_app, format_log)
		return StreamingHttpResponse(log) # 使用StreamingHttpResponse返回yield对象，实现实时浏览日志

# 获取supervisor程序的日志
@auth_controller
@accept_websocket
def tail_supervisor_app_log(request):
	global log_generator
	if not request.is_websocket():
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		supervisor_app = request.GET.get('supervisor_app')
		wsurl = request.get_host()+request.path
		server = Supervisor_Server.objects.filter(ip=server_ip).first()
		log_generator = server.tail_supervisor_app_log(supervisor_app)
		return render(request, 'tail_log.html', {'wsurl': wsurl})
	else:
		for log in log_generator:
			print (log)
			request.websocket.send(log)