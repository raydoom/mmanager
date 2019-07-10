# coding=utf8

import logging, os, configparser, json, requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator

from app.server.models import Server, ServerType
from app.jenkins.models import JobInfoCache
from app.jenkins.job import Job
from app.utils.common_func import auth_login_required
from app.utils.common_func import log_record
from app.utils.get_application_list import get_job_lists
from app.utils.paginator import paginator_for_list_view

# jenkins任务列表视图
@method_decorator(auth_login_required, name='dispatch')
class JobListView(View):
	def get(self, request):
		current_user_id = request.session.get('user_id')
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		try:
			server_type_id = ServerType.objects.get(server_type='jenkins').server_type_id
			servers = Server.objects.filter(server_type_id=server_type_id).order_by('host')
		except Exception as e:
			logging.error(e)
			servers = []
		job_list = []
		try:
			jobs = get_job_lists(servers)
			for job in jobs:
				job_info = JobInfoCache(
					host=job.host,
					host_port_api=job.host_port_api,
					host_protocal_api=job.host_protocal_api,
					name=job.name,
					color=job.color,
					current_user_id=current_user_id
					)
				job_list.append(job_info)
			JobInfoCache.objects.filter(current_user_id=current_user_id).delete()
			JobInfoCache.objects.bulk_create(job_list)
		except Exception as e:
			logging.error(e)
		if filter_keyword != None:
			if filter_select == 'Status =':
				job_lists = JobInfoCache.objects.filter(
					current_user_id=current_user_id,
					status=filter_keyword
					)
			if filter_select == 'Name':
				job_lists = JobInfoCache.objects.filter(
					current_user_id=current_user_id,
					name__icontains=filter_keyword
					)
			if filter_select == 'Host':
				job_lists = JobInfoCache.objects.filter(
					current_user_id=current_user_id,
					host__icontains=filter_keyword
					)
			page_prefix = '?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword + '&page='
		else:
			job_lists = JobInfoCache.objects.filter(current_user_id=current_user_id)
			page_prefix = '?page='
		page_num = request.GET.get('page')
		job_list = paginator_for_list_view(job_lists, page_num)
		curent_page_size = len(job_list)
		if filter_keyword == None:
			filter_keyword = ''
		if filter_select == None:
			filter_select = ''
		context = {
			'job_list': job_list, 
			'curent_page_size': curent_page_size, 
			'filter_keyword': filter_keyword, 
			'filter_select': filter_select, 
			'page_prefix': page_prefix
			}
		return render(request, 'job_list.html', context)

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/jenkins/job_list?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# jenkins操作
@method_decorator(auth_login_required, name='dispatch')
class JobOptionView(View):
	def get(self, request):
		host = request.GET.get('host')
		host_port_api = request.GET.get('host_port_api')
		job_name = request.GET.get('job_name')
		job_opt = request.GET.get('job_opt')
		server_type_id = ServerType.objects.get(server_type='jenkins').server_type_id
		server = Server.objects.get(server_type_id=server_type_id, host=host, port_api=host_port_api)
		job = Job()
		job.host = host
		job.host_port_api = host_port_api
		job.name = job_name
		job.host_username_api = server.username_api
		job.host_password_api = server.password_api
		job.host_protocal_api = server.protocal_api
		result = job.job_build_now(job_opt)
		log_detail = job_opt + ' <' + job_name + '> on host ' + host
		log_record(request.session.get('username'), log_detail=log_detail)
		return HttpResponse('200')

 	
