# coding=utf8

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
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		servers = Jenkins_Server.objects.all().order_by('ip')
		job_list = []
		for server in servers:
			try:
				jobs = server.get_all_jobs_list()
				if filter_keyword != None:
					for job in jobs:
						if filter_select == 'Status =' and filter_keyword.lower() == job['color'].lower():
								job_list.append(job)
						if filter_select == 'Name' and filter_keyword in job['name']:
								job_list.append(job)		
						if filter_select == 'Location' and filter_keyword in job['host_ip']:
								job_list.append(job)						
				else:
					for job in jobs:
						job_list.append(job)
			except Exception as e:
				logging.error(e)
		job_count = len(job_list)
		if filter_keyword == None:
			filter_keyword = ''
		if filter_select == None:
			filter_select = ''
		return render(request, 'jenkins_server.html', {'job_list': job_list, 'job_count': job_count, 'filter_keyword': filter_keyword, 'filter_select': filter_select})

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/jenkinsserver/?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)


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
		return HttpResponse(result)

 	
