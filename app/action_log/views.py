# coding=utf8

from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.decorators import method_decorator

from app.utils.common_func import auth_login_required
from app.utils.common_func import get_dir_info
from app.utils.common_func import get_file_contents
from app.utils.common_func import log_record
from app.action_log.models import ActionLog
from app.utils.paginator import paginator_for_list_view

# 操作日志查看页面试图函数
@method_decorator(auth_login_required, name='dispatch')
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
		page_num = request.GET.get('page')
		action_log = paginator_for_list_view(action_logs ,page_num)
		curent_page_size = len(action_log)
		context = {
			'action_log': action_log,
			'curent_page_size': curent_page_size, 
			'page_prefix': page_prefix
			}
		return render(request, 'action_log.html', context)

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/action_log/action_log_list?filter_select=' + filter_select +'&filter_keyword=' + filter_keyword
		return redirect(prg_url)