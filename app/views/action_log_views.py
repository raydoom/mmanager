from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging, os, configparser, json

from ..utils.common_func import auth_controller, get_dir_info, get_file_contents, log_record
from ..models.action_log_models import Action_Log

# 操作日志查看页面试图函数
@method_decorator(auth_controller, name='dispatch')
class Action_Log_List(View):
	def get(self, request):
		action_logs = Action_Log.objects.all().order_by('-log_time')
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
		return render(request, 'action_log.html', {'action_log': action_log, 'action_log_count': action_log_count})

