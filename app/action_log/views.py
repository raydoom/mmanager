# coding=utf8

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging, os, configparser, json

from app.utils.common_func import auth_controller, get_dir_info, get_file_contents, log_record
from app.action_log.models import ActionLog

# 操作日志查看页面试图函数
@method_decorator(auth_controller, name='dispatch')
class ActionLogListView(View):
	def get(self, request):
		req_url = request.get_full_path()
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		if filter_keyword != None:
			if filter_select == 'User =':
				action_logs = ActionLog.objects.filter(log_user=filter_keyword).order_by('-log_time')
			if filter_select == 'Detail':
				action_logs = ActionLog.objects.filter(log_detail__icontains=filter_keyword).order_by('-log_time')
			page_prefix = '?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword + '&page='
		else:
			action_logs = ActionLog.objects.all().order_by('-log_time')
			page_prefix = '?page='
		paginator = Paginator(action_logs, 10)
		page = request.GET.get('page')
		try:
			action_log = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			action_log = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			action_log = paginator.page(paginator.num_pages)
		action_log_count = len(action_logs)
		return render(request, 'action_log.html', {'action_log': action_log, 'action_log_count': action_log_count, 'page_prefix': page_prefix})

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/action_log/action_log_list?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)