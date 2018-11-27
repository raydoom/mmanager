from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
import logging, os, configparser, json

from ..models.jenkins_server_models import Jenkins_Server
from ..utils.common_func import format_log, auth_controller, get_dir_info, get_file_contents, log_record


# jenkins任务列表视图
@method_decorator(auth_controller, name='dispatch')
class Jenkins_Server_List(View):
	def get(self, request):
		servers = Jenkins_Server.objects.all().order_by('ip')
		job_list = []
		for server in servers:
			jobs = server.get_all_jobs_list()
			for job in jobs:
				job_list.append(job)
		job_count = len(job_list)
		return render(request, 'jenkins_server.html', {'job_list': job_list, 'job_count': job_count})


# jenkins操作
@method_decorator(auth_controller, name='dispatch')
class Jenkins_Job_Opt(View):
	def get(self, request):
		server_ip = request.GET.get('server_ip')
		server_port = int(request.GET.get('server_port'))
		job_name = request.GET.get('job_name')
		jenkins_opt = request.GET.get('jenkins_opt')
		server = Jenkins_Server.objects.filter(ip=server_ip).first()
		result = server.send_build_job(job_name)
		log_detail = jenkins_opt + ' <' + job_name + '> on host ' + server_ip
		log_record(request.session.get('username'), log_detail=log_detail)
		return redirect('/jenkinsservers/')

 	
