# coding=utf8

from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
import logging, json, time, threading
from dwebsocket import require_websocket, accept_websocket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.server.models import Server, ServerType
from app.supervisor.process import Process
from app.supervisor.models import ProcessInfo
from app.utils.common_func import get_time_stamp, format_log, auth_controller, log_record, send_data_over_websocket
from app.utils.get_application_list import get_process_lists


# 获取supervisor服务器及程序列表，根据选项和关键字过滤
@method_decorator(auth_controller, name='dispatch')
class ProcessListView(View):
	def get(self, request):
		current_user_id = request.session.get('user_id')
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		servers = ServerType.objects.get(server_type='supervisor').server_set.all().order_by('ip')
		process_list = []
		try:
			processes = get_process_lists(servers)
			for process in processes:
				process_list.append(ProcessInfo(host_ip=process.host_ip,
												host_port=process.host_port,
												host_username=process.host_username,
												host_password=process.host_password,
												statename=process.statename,
												name=process.name,
												description=process.description,
												current_user_id=current_user_id))
			ProcessInfo.objects.filter(current_user_id=current_user_id).delete()
			ProcessInfo.objects.bulk_create(process_list)
		except Exception as e:
			logging.error(e)		
		if filter_keyword != None:
			if filter_select == 'Status =':
				process_list = ProcessInfo.objects.filter(current_user_id=current_user_id,status=filter_keyword)
			if filter_select == 'Name':
				process_list = ProcessInfo.objects.filter(current_user_id=current_user_id,name__icontains=filter_keyword)
			if filter_select == 'Location':
				process_list = ProcessInfo.objects.filter(current_user_id=current_user_id,host_ip__icontains=filter_keyword)
			page_prefix = '?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword + '&page='
		else:
			process_list = ProcessInfo.objects.filter(current_user_id=current_user_id)
			page_prefix = '?page='
		paginator = Paginator(process_list, 10)
		page = request.GET.get('page')
		try:
			process_list = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			process_list = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			process_list = paginator.page(paginator.num_pages)
		process_count = len(process_list)
		if filter_keyword == None:
			filter_select = ''
			filter_keyword = ''
		return render(request, 'process_list.html', {'process_list': process_list, 'process_count': process_count, 'filter_keyword': filter_keyword, 'filter_select': filter_select, 'page_prefix': page_prefix})

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/supervisor/process_list?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# supervisor程序操作启动，停止，重启
@method_decorator(auth_controller, name='dispatch')
class ProcessOptionView(View):
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
def process_log(request):
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








			