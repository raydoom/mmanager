from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required

import docker, logging, os, configparser, json

from ..models.docker_server_models import  Docker_Server
from ..models.server import Server, ServerType
from ..models.supervisor_server_models import  Supervisor_Server
from ..models.jenkins_server_models import  Jenkins_Server
from ..utils.common_func import auth_controller, log_record

# 所有服务器列表
@method_decorator(auth_controller, name='dispatch')
class Server_List(View):
	def get(self, request):
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		server_list = []
		server_list_filter = []
		for server in  ServerType.objects.get(server_type='docker').server_set.all().order_by('ip'):
			server.type = 'docker'
			try:
				result = server.get_container_list()
				server.status = 'Connected'
				result_running = 0
				for i in result:
					if i.statename == 'running':
						result_running +=1
				server.description = str(len(result)) + ' containers, ' + str(result_running) + ' running'
			except Exception as e:
				logging.error(e)
				server.status = 'Disonnected'
			server_list.append(server)
		for server in  ServerType.objects.get(server_type='supervisor').server_set.all().order_by('ip'):
			server.type = 'supervisor'
			result = server.get_process_list()
			if result == None:
				server.status = 'Disconnected'
			else:
				server.status = 'Connected'
				result_running = 0
				for i in result:
					if i.statename == 'RUNNING':
						result_running +=1
				server.description = str(len(result)) + ' apps, ' + str(result_running) + ' running'
			server_list.append(server)
		for server in Jenkins_Server.objects.all().order_by('ip'):
			server.type = 'jenkins'
			result = server.get_all_jobs_list()
			if result == None:
				server.status = 'Disconnected'
			else:
				server.status = 'Connected'
				result_blue = 0
				for i in result:
					if i['color'] == 'blue':
						result_blue +=1
				server.description = str(len(result)) + ' jobs, ' + str(result_blue) + ' blue'
			server_list.append(server)
		if filter_keyword != None:
			for server in server_list:
				if filter_select == 'Host Name' and filter_keyword in server.hostname:
					server_list_filter.append(server)
				if filter_select == 'IP' and filter_keyword in server.ip:
					server_list_filter.append(server)
				if filter_select == 'Port =' and int(filter_keyword) == server.port:
					server_list_filter.append(server)
				if filter_select == 'Type =' and filter_keyword == server.type:
					server_list_filter.append(server)
			server_list = server_list_filter

		server_count = len(server_list)
		return render(request, 'server_list.html', {'server_list': server_list, 'server_count': server_count})

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/serverlist/?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# 添加服务器
@method_decorator(auth_controller, name='dispatch')
class Add_Server(View):
	def get(self, request):
		return render(request, 'add_server.html')

	def post(self, request):
		hostname = request.POST.get('hostname')
		server_type = request.POST.get('server_type')
		ip = request.POST.get('ip')
		port = request.POST.get('port')
		apiversion = request.POST.get('apiversion')
		username = request.POST.get('username')
		password = request.POST.get('password')
		description = request.POST.get('description')
		if server_type == 'Docker' or server_type == 'Supervisor':
			server_type_get = ServerType.objects.get(server_type=server_type.lower())
			new_server = Server(hostname=hostname, ip=ip, port=int(port), username=username, password=password, description=description)
			new_server.save()
			new_server.server_type.add(server_type_get)
			new_server.save()

		if server_type == 'Jenkins':
			Jenkins_Server.objects.create(hostname=hostname, ip=ip, port=int(port), apiversion=apiversion, username=username, password=password, description=description)
		return redirect('/serverlist/')

# 删除服务器
@method_decorator(auth_controller, name='dispatch')
class Delete_Server(View):
	def get(self, request):
		server_type = request.GET.get('servertype')
		ip = request.GET.get('ip')
		port = request.GET.get('port')
		if server_type == 'docker' or server_type == 'supervisor':
			ServerType.objects.get(server_type=server_type).server_set.all().filter(ip=ip, port=int(port)).delete()

		if server_type == 'jenkins':
			Jenkins_Server.objects.filter(ip=ip, port=int(port)).delete()
		return redirect('/serverlist/')