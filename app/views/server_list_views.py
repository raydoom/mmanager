from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required

import docker, logging, os, configparser, json

from ..models.docker_server_models import  Docker_Server
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
		for server in Docker_Server.objects.all().order_by('ip'):
			server.type = 'docker'
			server_list.append(server)
		for server in Supervisor_Server.objects.all().order_by('ip'):
			server.type = 'supervisor'
			server_list.append(server)
		for server in Jenkins_Server.objects.all().order_by('ip'):
			server.type = 'jenkins'
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