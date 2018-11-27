from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging, os, configparser, json

from ..utils.common_func import auth_controller, get_dir_info, get_file_contents, log_record
from django.conf import settings


# 获取cconfig.ini中的配置项
CONF_DIRS=(settings.BASE_DIR+'/config')
conf_dir = configparser.ConfigParser()
conf_dir.read(CONF_DIRS+'/config.ini')

dir_root = conf_dir.get('dir_info', 'dir_root')
lines_per_page = int(conf_dir.get('dir_info', 'lines_per_page'))


## 本地日志目录浏览
@method_decorator(auth_controller, name='dispatch')
class Directory_Viewer(View):
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
		return render(request, 'directory_viewer.html', {'dir_infos': dir_infos, 'current_dir': current_dir, 'dir_infos_count': dir_infos_count})


# 本地日志文件浏览
@method_decorator(auth_controller, name='dispatch')
class Text_Viewer(View):
	def get(self, request):
		dist = dir_root
		if request.GET.get('dist'):
			dist = request.GET.get('dist')
			dist = dir_root + dist
		text_contents = []
		text_contents = get_file_contents(dist, lines_per_page)
		log_user=request.session.get('username')
		log_detail=log_user + ' viewer ' + dist
		log_record(log_user=log_user, log_detail=log_detail)
		return render(request, 'text_viewer.html', {'text_contents': text_contents})


# 文件下载视图函数
@method_decorator(auth_controller, name='dispatch')
class File_Download(View):
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


 	
