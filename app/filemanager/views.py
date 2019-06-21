# coding=utf8

import os
import logging
import json
import configparser
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import FileResponse
from django.http import StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from dwebsocket import require_websocket
from dwebsocket import accept_websocket

from app.utils.common_func import auth_login_required
from app.utils.common_func import get_dir_info
from app.utils.common_func import get_file_contents
from app.utils.common_func import log_record
from django.conf import settings
from app.utils.config_info_formater import ConfigInfo

# 获取配置文件按信息
config = ConfigInfo()
dir_root = config.config_info.get('dir_info').get('dir_root')
lines_per_page = int(config.config_info.get('dir_info').get('lines_per_page'))

# 本地日志目录浏览
@method_decorator(auth_login_required, name='dispatch')
class DirectoryListView(View):
	def get(self, request):
		dist = '/'
		current_dir = '/'
		if request.GET.get('dist'):
			dist = request.GET.get('dist') + '/'
			if dist.split('/')[-2] == '..': 
				dist_list = dist.split('/')
				dist = ''
				for i in range(0,len(dist_list)-3):
					dist = dist + dist_list[i] +'/'
		current_dir = dist			
		dist = dir_root + dist	
		dir_infos = get_dir_info(dist)
		dir_infos_count = len(dir_infos)
		context = {
			'dir_infos': dir_infos, 
			'current_dir': current_dir, 
			'dir_infos_count': dir_infos_count}
		return render(request, 'directory_list.html', context)

# 本地文本文件浏览
@method_decorator(auth_login_required, name='dispatch')
class TextViewerView(View):
	def get(self, request):
		current_directory = '/'
		dist = dir_root
		if request.GET.get('dist'):
			dist = request.GET.get('dist')
			current_directory = request.GET.get('dist')
			dist = dir_root + dist
		page = 1
		if request.GET.get('page'):
			page = int(request.GET.get('page'))
		text_contents = []
		filter_keyword = request.GET.get('filter_keyword', '')
		filter_select = request.GET.get('filter_select', '')
		text_contents, total_pages = get_file_contents(dist, lines_per_page, page, filter_keyword)
		log_user=request.session.get('username')
		log_detail=log_user + ' viewer ' + dist
		log_record(log_user=log_user, log_detail=log_detail)
		page_prefix = ('?dist=' + request.GET.get('dist') + '&filter_select=' + 
						filter_select + '&filter_keyword=' + filter_keyword + '&page=')
		previous_page_number = page - 1
		if previous_page_number < 1:
			previous_page_number = 1
		next_page_number = page + 1
		if next_page_number > total_pages:
			next_page_number = total_pages
		current_page_number = page
		context = {
			'text_contents': text_contents,
			'current_directory': current_directory,
			'page_prefix': page_prefix,
			'next_page_number': next_page_number,
			'page_prefix': page_prefix,
			'previous_page_number': previous_page_number,
			'current_page_number': current_page_number,
			'total_pages': total_pages,
			'filter_select': filter_select,
			'filter_keyword': filter_keyword}
		return render(request, 'text_viewer.html', context)
	def post(self, request):
		dist = request.POST.get('dist')
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = ('/filemanager/text_viewer?dist=' + dist + '&filter_select=' + 
					filter_select +'&filter_keyword=' + filter_keyword + '&page=1')
		return redirect(prg_url)

# 文件下载视图函数
@method_decorator(auth_login_required, name='dispatch')
class FileDownloadView(View):
	def get(self, request):
		filepath = request.GET.get('filepath')
		filepath = dir_root + filepath
		file=open(filepath, 'rb')
		response =FileResponse(file)
		response['Content-Type']='application/octet-stream'
		filename = filepath.split('/')[-1]
		Content_Disposition = 'attachment;filename=' + filename
		response['Content-Disposition']=Content_Disposition
		log_detail='download ' + filepath
		log_record(request.session.get('username'), log_detail=log_detail)
		return response 
