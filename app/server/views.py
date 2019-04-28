# coding=utf8

from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required

import logging, os, configparser, json

from app.server.models import Server, ServerType
from app.jenkins.models import  JenkinsServer
from app.utils.common_func import auth_controller, log_record
from app.utils.get_application_list import get_container_lists, get_process_lists

# 所有服务器列表
@method_decorator(auth_controller, name='dispatch')
class ServerListView(View):
	def get(self, request):
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		server_list = []
		server_list_filter = []
		for server in  ServerType.objects.get(server_type='docker').server_set.all().order_by('ip'):
			# get_container_list只能接受列表参数，无法接受单个对象作为参数，生成只含一个server对象的列表server_list_odd
			server_list_odd = []
			server_list_odd.append(server)
			server.type = server.server_type.first()
			try:
				result = get_container_lists(server_list_odd)
				server.status = 'Connected'
				result_running = 0
				for i in result:
					if i.statename == 'running':
						result_running +=1
				server.description = str(len(result)) + ' containers, ' + str(result_running) + ' running'
			except Exception as e:
				logging.error(e)
				server.status = 'Disonnected'
				server.description = 'none'
			server_list.append(server)
		for server in  ServerType.objects.get(server_type='supervisor').server_set.all().order_by('ip'):
			server_list_odd = []
			server_list_odd.append(server)
			server.type = server.server_type.first()
			try:
				result = get_process_lists(server_list_odd)
				server.status = 'Connected'
				result_running = 0
				for i in result:
					if i.statename == 'RUNNING':
						result_running +=1
				server.description = str(len(result)) + ' processes, ' + str(result_running) + ' running'
			except Exception as e:
				logging.error(e)
				server.status = 'Disonnected'	
				server.description = 'none'			
			server_list.append(server)
		for server in JenkinsServer.objects.all().order_by('ip'):
			server.type = 'jenkins'
			try:
				result = server.get_all_jobs_list()
				server.status = 'Connected'
				result_blue = 0
				for i in result:
					if i['color'] == 'blue':
						result_blue +=1
				server.description = str(len(result)) + ' jobs, ' + str(result_blue) + ' blue'
			except Exception as e:
				logging.error(e)
				server.status = 'Disonnected'	
				server.description = 'none'
			server_list.append(server)
		if filter_keyword != None:
			for server in server_list:
				if filter_select == 'Host Name' and filter_keyword in server.hostname:
					server_list_filter.append(server)
				if filter_select == 'IP' and filter_keyword in server.ip:
					server_list_filter.append(server)
				if filter_select == 'Port =' and int(filter_keyword) == server.port:
					server_list_filter.append(server)
				if filter_select == 'Type =' and filter_keyword == str(server.type):
					server_list_filter.append(server)
			server_list = server_list_filter
		server_count = len(server_list)
		if filter_keyword == None:
			filter_keyword = ''
		if filter_select == None:
			filter_select = ''
		return render(request, 'server_list.html', {'server_list': server_list, 'server_count': server_count, 'filter_keyword': filter_keyword, 'filter_select': filter_select})

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = 'server/server_list?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# 添加服务器
@method_decorator(auth_controller, name='dispatch')
class ServerCreateView(View):
	def get(self, request):
		return render(request, 'server_create.html')

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
			JenkinsServer.objects.create(hostname=hostname, ip=ip, port=int(port), apiversion=apiversion, username=username, password=password, description=description)
		return redirect('/server/server_list')

# 删除服务器
@method_decorator(auth_controller, name='dispatch')
class ServerDeleteView(View):
	def get(self, request):
		server_type = request.GET.get('servertype')
		ip = request.GET.get('ip')
		port = request.GET.get('port')
		if server_type == 'docker' or server_type == 'supervisor':
			ServerType.objects.get(server_type=server_type).server_set.all().filter(ip=ip, port=int(port)).delete()

		if server_type == 'jenkins':
			JenkinsServer.objects.filter(ip=ip, port=int(port)).delete()
		return redirect('/server/server_list')

# 编辑服务器
@method_decorator(auth_controller, name='dispatch')
class ServerUpdateView(View):
	def get(self, request):
		server_type = request.GET.get('servertype')
		ip = request.GET.get('ip')
		port = request.GET.get('port')
		if server_type == 'docker' or server_type == 'supervisor':		
			server = ServerType.objects.get(server_type=server_type).server_set.get(ip=ip,port=int(port))
			server_type = server.server_type.all().first().server_type.capitalize()
			return render(request, 'server_update.html', {'server': server, 'server_type': server_type})
		if server_type == 'jenkins':
			return HttpResponse('...')

	def post(self, request):
		hostname = request.POST.get('hostname')
		server_type = request.POST.get('server_type')
		ip = request.POST.get('ip')
		port = request.POST.get('port')
		apiversion = request.POST.get('apiversion','')
		username = request.POST.get('username')
		password = request.POST.get('password')
		description = request.POST.get('description')
		if server_type == 'Docker' or server_type == 'Supervisor':
			server_type_get = ServerType.objects.get(server_type=server_type.lower())
			obj = ServerType.objects.get(server_type=server_type_get).server_set.all().filter(ip=ip, port=int(port)).first()
			obj.hostname=hostname
			obj.ip=ip
			obj.port=int(port)
			obj.username=username
			obj.description = description
			if password != '':
				obj.password = password
			obj.save()
		if server_type == 'Jenkins':
			pass
		return redirect('/server/server_list')