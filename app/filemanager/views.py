# coding=utf8

import os
import logging
import json
import re
import configparser
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import FileResponse
from django.http import StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator

from app.server.models import Server
from app.server.models import ServerType
from app.utils.common_func import auth_login_required
from app.utils.common_func import get_dir_info
from app.utils.common_func import get_file_contents
from app.utils.common_func import log_record
from app.utils.common_func import exec_command_over_ssh
from app.utils.common_func import transfer_file_over_sftp
from app.filemanager.directory import Directory
from app.utils.config_info_formater import ConfigInfo
from app.utils.paginator import paginator_for_list_view

# 获取配置文件按信息
config = ConfigInfo()
tmp_path = config.config_info.get('path_info').get('tmp_path')
lines_for_view = (config.config_info.get('path_info').get('lines_for_view'))

# 文本文件浏览
@method_decorator(auth_login_required, name='dispatch')
class TextViewerView(View):
	def get(self, request):
		filter_keyword = request.GET.get('filter_keyword', '')
		filter_select = request.GET.get('filter_select', '')
		host = request.GET.get('host', '')
		server_type_id = ServerType.objects.get(server_type='file').server_type_id
		server = Server.objects.get(server_type_id=server_type_id,host=host)
		path_root = server.file_path_root
		path = request.GET.get('path')		
		cmd_tail = 'tail -' + lines_for_view + ' ' + path_root + path	
		if filter_select == 'Content' and filter_keyword != '':
			cmd_tail = cmd_tail + ' | grep ' + filter_keyword
		text_content = exec_command_over_ssh(
			server.host,
			server.port,
			server.username,
			server.password,
			cmd=cmd_tail,
			)
		try:
			text_content = text_content.decode(encoding='utf8')
		except Exception as e:
			logging.error(e)
			text_content = 'can not decode file content'
		log_user=request.session.get('username')
		log_detail=log_user + ' viewer ' + path
		log_record(log_user=log_user, log_detail=log_detail)
		context = {
			'host': host,
			'path': path,
			'text_content': text_content,
			'filter_select': filter_select,
			'filter_keyword': filter_keyword
			}
		return render(request, 'text_viewer.html', context)

	def post(self, request):
		path = request.POST.get('path')
		host = request.POST.get('host', '')
		filter_keyword = request.POST.get('filter_keyword', '')
		filter_select = request.POST.get('filter_select', '')
		prg_url = (
			'/filemanager/text_viewer?host='
			+ host
			+ '&path='
			+ path
			+ '&filter_select='
			+ filter_select
			+ '&filter_keyword='
			+ filter_keyword
			)
		return redirect(prg_url)

# 文件下载视图函数
@method_decorator(auth_login_required, name='dispatch')
class FileDownloadView(View):
	def get(self, request):
		host = request.GET.get('host', '')
		server_type_id = ServerType.objects.get(server_type='file').server_type_id
		server = Server.objects.get(server_type_id=server_type_id,host=host)
		path_root = server.file_path_root
		path = request.GET.get('path')
		filename = path.split('/')[-1]
		remote_file_path = path_root + path
		local_file_path = tmp_path + '/' + filename
		transfer_file_over_sftp(
			server.host,
			server.port,
			server.username,
			server.password,
			remote_path=remote_file_path,
			local_path=local_file_path,
			)
		file=open(local_file_path, 'rb')
		response =FileResponse(file)
		response['Content-Type']='application/octet-stream'
		Content_Disposition = 'attachment;filename=' + filename
		response['Content-Disposition']=Content_Disposition
		log_detail='download ' + path + ' on host ' + host
		log_record(request.session.get('username'), log_detail=log_detail)
		return response 

# 文件服务器列表
@method_decorator(auth_login_required, name='dispatch')
class FileServerListView(View):
	def get(self, request):
		req_url = request.get_full_path()
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		server_type_id = ServerType.objects.get(server_type='file').server_type_id
		if filter_keyword != None:
			if filter_select == 'Host':
				file_servers = Server.objects.filter(
					server_type_id=server_type_id,
					host__icontains=filter_keyword
					)
			if filter_select == 'Port =':
				file_servers = Server.objects.filter(
					server_type_id=server_type_id,
					port=int(filter_keyword)
					)
			page_prefix = '?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword + '&page='
		else:
			file_servers = Server.objects.filter(server_type_id=server_type_id).order_by('host')
			page_prefix = '?page='
		page_num = request.GET.get('page')
		file_server = paginator_for_list_view(file_servers, page_num)
		current_page_size = len(file_server)
		if filter_keyword == None:
			filter_select = ''
			filter_keyword = ''
		context = {
			'file_server': file_server,
			'current_page_size': current_page_size,
			'page_prefix': page_prefix,
			'filter_select': filter_select,
			'filter_keyword': filter_keyword,
			}
		return render(request, 'file_server_list.html', context)

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword', '')
		filter_select = request.POST.get('filter_select', '')
		prg_url = '/filemanager/file_server_list?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# 目录列表
@method_decorator(auth_login_required, name='dispatch')
class DirectoryListView(View):
	def get(self, request):
		host = request.GET.get('host', '')
		server_type_id = ServerType.objects.get(server_type='file').server_type_id
		server = Server.objects.get(server_type_id=server_type_id,host=host)
		path_root = server.file_path_root
		path = request.GET.get('path', '')
		absolutely_path = path_root + path
		# 返回上级目录，生成上级目录路径
		path_end = re.split('/+', path)[-1]
		parent_path = path.rstrip(path_end).rstrip('/')
		directory = Directory()
		directory.host = server.host
		directory.host_port = server.port
		directory.host_username = server.username
		directory.host_password = server.password
		file_list_orgin = directory.get_file_list(path=absolutely_path)
		file_list = []
		for file_info in file_list_orgin:
			file = {}
			file_info = re.split(' +', file_info)
			file['file_type'] = file_info[0]
			file['file_link_count'] = file_info[1]
			file['file_owner'] = file_info[2]
			file['file_group'] = file_info[3]
			file['file_size'] = file_info[4]
			file['file_mtime'] = file_info[5] + ' ' + file_info[6] + ' ' + file_info[7]
			file['file_name'] = file_info[8]
			file['file_host'] = host
			if file['file_type'][0] == 'd':
				file['is_directory'] = 1
			else:
				file['is_directory'] = 0
			file_list.append(file)
		file_list_count = len(file_list)
		context = {
			'host': host,
			'file_list': file_list, 
			'file_list_count': file_list_count,
			'path': path,
			'parent_path': parent_path
			}
		return render(request, 'directory_list.html', context)

