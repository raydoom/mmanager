# coding=utf8

from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
import logging, json, time, threading
from dwebsocket import require_websocket, accept_websocket

from app.server.models import Server, ServerType
from app.supervisor.process import Process
from app.supervisor.models import ProcessInfoCache
from app.utils.common_func import get_time_stamp, format_log, auth_controller, log_record, send_data_over_websocket
from app.utils.get_application_list import get_process_lists
from app.utils.paginator import paginator_for_list_view


# 获取supervisor服务器及程序列表，根据选项和关键字过滤
@method_decorator(auth_controller, name='dispatch')
class ProcessListView(View):
	def get(self, request):
		current_user_id = request.session.get('user_id')
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		server_type_id = ServerType.objects.get(server_type='supervisor').server_type_id
		servers = Server.objects.filter(server_type_id=server_type_id).order_by('host')
		process_list = []
		try:
			processes = get_process_lists(servers)
			for process in processes:
				process_list.append(ProcessInfoCache(host=process.host,
												host_port=process.host_port,
												statename=process.statename,
												name=process.name,
												description=process.description,
												current_user_id=current_user_id))
			ProcessInfoCache.objects.filter(current_user_id=current_user_id).delete()
			ProcessInfoCache.objects.bulk_create(process_list)
		except Exception as e:
			logging.error(e)		
		if filter_keyword != None:
			if filter_select == 'Status =':
				process_lists = ProcessInfoCache.objects.filter(current_user_id=current_user_id,status=filter_keyword)
			if filter_select == 'Name':
				process_lists = ProcessInfoCache.objects.filter(current_user_id=current_user_id,name__icontains=filter_keyword)
			if filter_select == 'Host':
				process_lists = ProcessInfoCache.objects.filter(current_user_id=current_user_id,host__icontains=filter_keyword)
			page_prefix = '?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword + '&page='
		else:
			process_lists = ProcessInfoCache.objects.filter(current_user_id=current_user_id)
			page_prefix = '?page='
		page_num = request.GET.get('page')
		process_list = paginator_for_list_view(process_lists, page_num)
		curent_page_size = len(process_list)
		if filter_keyword == None:
			filter_select = ''
			filter_keyword = ''
		return render(request, 'process_list.html', {'process_list': process_list, 'curent_page_size': curent_page_size, 'filter_keyword': filter_keyword, 'filter_select': filter_select, 'page_prefix': page_prefix})

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/supervisor/process_list?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# supervisor程序操作启动，停止，重启
@method_decorator(auth_controller, name='dispatch')
class ProcessOptionView(View):
	def get(self, request):
		host = request.GET.get('host')
		host_port = int(request.GET.get('host_port'))
		process_name = request.GET.get('process_name')
		process_opt = request.GET.get('process_opt')
		server_type_id = ServerType.objects.get(server_type='supervisor').server_type_id
		server = Server.objects.get(server_type_id=server_type_id, host=host, port=host_port)
		process = Process()
		process.host = server.host
		process.host_port = server.port
		process.host_username = server.username
		process.host_password = server.password
		process.name = process_name		
		result = process.process_opt(process_opt)
		log_detail = process_opt + ' <' + process_name + '> on host ' + host
		log_record(request.session.get('username'), log_detail=log_detail)
		return HttpResponse(result)

# 获取supervisor程序的日志
@auth_controller
@accept_websocket
def process_log(request):
	if not request.is_websocket():
		host = request.GET.get('host')
		host_port = int(request.GET.get('host_port'))
		process_name = request.GET.get('process_name')
		return render(request, 'tail_log.html', {'name': process_name, 'host': host})
	else:
		host = request.GET.get('host')
		host_port = int(request.GET.get('host_port'))
		process_name = request.GET.get('process_name')
		server_type_id = ServerType.objects.get(server_type='supervisor').server_type_id
		server = Server.objects.get(server_type_id=server_type_id, host=host, port=host_port)
		process = Process()
		process.host = server.host
		process.host_port = server.port
		process.host_username = server.username
		process.host_password = server.password
		process.process_name = process_name		
		channel = process.tail_process_logs()
		# 为每个websocket连接开启独立线程
		t = threading.Thread(target=send_data_over_websocket, args=(request,channel))
		t.start()
		t.join()








			