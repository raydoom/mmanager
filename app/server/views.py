# coding=utf8

import logging
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.decorators import method_decorator

from app.server.models import Server
from app.server.models import ServerType
from app.server.models import ServerInfoCache
from app.filemanager.directory import Directory
from app.utils.common_func import auth_login_required
from app.utils.common_func import log_record
from app.utils.get_application_list import get_process_lists
from app.utils.get_application_list import get_job_lists
from app.utils.data_encrypter import DataEncrypter
from app.utils.paginator import paginator_for_list_view

# 所有服务器列表
@method_decorator(auth_login_required, name='dispatch')
class ServerListView(View):
	def get(self, request):
		current_user_id = request.session.get('user_id')
		filter_keyword = request.GET.get('filter_keyword')
		filter_select = request.GET.get('filter_select')
		server_list = []
		server_lists = []
		# docker服务器
		try:
			server_type_id = ServerType.objects.get(server_type='docker').server_type_id
			servers = Server.objects.filter(server_type_id=server_type_id).order_by('host')
		except Exception as e:
			logging.error(e)
			servers = []
		for server in servers:
			# get_container_list只能接受列表参数，无法接受单个对象作为参数，
			# 生成只含一个server对象的列表server_list_odd
			server_list_odd = []
			server_list_odd.append(server)
			server.type = 'docker'
			try:
				result = get_container_lists(server_list_odd)
				server.status = 'Connected'
				result_running = 0
				for i in result:
					if i.statename == 'running':
						result_running += 1
				server.description = str(len(result)) + ' containers, ' + str(result_running) + ' running'
			except Exception as e:
				logging.error(e)
				server.status = 'Disonnected'
				server.description = 'none'
			server_lists.append(server)
		# supervisor服务器
		try:
			server_type_id = ServerType.objects.get(server_type='supervisor').server_type_id
			servers = Server.objects.filter(server_type_id=server_type_id).order_by('host')
		except Exception as e:
			logging.error(e)
			servers = []
		for server in servers:
			server_list_odd = []
			server_list_odd.append(server)
			server.type = 'supervisor'
			try:
				result = get_process_lists(server_list_odd)
				server.status = 'Connected'
				result_running = 0
				for i in result:
					if i.statename == 'RUNNING':
						result_running += 1
				server.description = str(len(result)) + ' processes, ' + str(result_running) + ' running'
			except Exception as e:
				logging.error(e)
				server.status = 'Disonnected'	
				server.description = 'none'			
			server_lists.append(server)
		# jenkins服务器
		try:
			server_type_id = ServerType.objects.get(server_type='jenkins').server_type_id
			servers = Server.objects.filter(server_type_id=server_type_id).order_by('host')
		except Exception as e:
			logging.error(e)
			servers = []
		for server in servers:
			server_list_odd = []
			server_list_odd.append(server)
			server.type = 'jenkins'
			try:
				result = get_job_lists(server_list_odd)
				server.status = 'Connected'
				result_blue = 0
				for i in result:
					if i.color == 'blue':
						result_blue += 1
				server.description = str(len(result)) + ' jobs, ' + str(result_blue) + ' blue'
			except Exception as e:
				logging.error(e)
				server.status = 'Disonnected'
				server.description = 'none'
			server_lists.append(server)
		# file服务器
		try:
			server_type_id = ServerType.objects.get(server_type='file').server_type_id
			servers = Server.objects.filter(server_type_id=server_type_id).order_by('host')
		except Exception as e:
			logging.error(e)
			servers = []
		for server in servers:
			server.type = 'file'
			try:
				directory = Directory()
				directory.host = server.host
				directory.host_port = server.port
				directory.host_username = server.username
				directory.host_password = server.password
				path_root = server.file_path_root
				file_list_orgin = directory.get_file_list(path=path_root)
				if len(file_list_orgin) != 0:
					server.status = 'Connected'
				else:
					server.status = 'Disonnected'
			except Exception as e:
				logging.error(e)
				server.status = 'Disonnected'
			server_lists.append(server)
		try:
			for server in server_lists:
				server_info_cache = ServerInfoCache(
					host=server.host,
					port=server.port,
					server_id=server.server_id,
					server_type=server.type,
					description=server.description,
					port_api=server.port_api,
					protocal_api=server.protocal_api,
					status=server.status,
					current_user_id=current_user_id
					)
				server_list.append(server_info_cache)
			ServerInfoCache.objects.filter(current_user_id=current_user_id).delete()
			ServerInfoCache.objects.bulk_create(server_list)
		except Exception as e:
			logging.error(e)
		if filter_keyword != None:
			if filter_select == 'Status =':
				server_lists = ServerInfoCache.objects.filter(
					current_user_id=current_user_id,
					status=filter_keyword
					)
			if filter_select == 'Port =':
				server_lists = ServerInfoCache.objects.filter(
					current_user_id=current_user_id,
					port=int(filter_keyword)
					)
			if filter_select == 'Host':
				server_lists = ServerInfoCache.objects.filter(
					current_user_id=current_user_id,
					host__icontains=filter_keyword
					)
			if filter_select == 'Type =':
				server_lists = ServerInfoCache.objects.filter(
					current_user_id=current_user_id,
					server_type=filter_keyword
					)
			page_prefix = '?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword + '&page='
		else:
			server_lists = ServerInfoCache.objects.filter(current_user_id=current_user_id)
			page_prefix = '?page='
		page_num = request.GET.get('page')
		server_list = paginator_for_list_view(server_lists, page_num)
		curent_page_size = len(server_list)
		if filter_keyword == None:
			filter_select = ''
			filter_keyword = ''
		context = {
			'server_list': server_list,
			'curent_page_size':curent_page_size,
			'filter_keyword': filter_keyword,
			'filter_select': filter_select,
			'page_prefix': page_prefix
			}
		return render(request, 'server_list.html', context)

	def post(self, request):
		filter_keyword = request.POST.get('filter_keyword')
		filter_select = request.POST.get('filter_select')
		prg_url = '/server/server_list?filter_select=' + filter_select + '&filter_keyword=' + filter_keyword
		return redirect(prg_url)

# 添加服务器
@method_decorator(auth_login_required, name='dispatch')
class ServerCreateView(View):
	def get(self, request):
		return render(request, 'server_create.html')

	def post(self, request):
		host = request.POST.get('host')
		port = request.POST.get('port')
		username = request.POST.get('username')
		password = request.POST.get('password')
		username_api = request.POST.get('username_api')
		password_api = request.POST.get('password_api')
		port_api = request.POST.get('port_api')
		protocal_api = request.POST.get('protocal_api')
		file_path_root = request.POST.get('file_path_root')
		description = request.POST.get('description')
		server_type = request.POST.get('server_type')
		server_type_id = int(ServerType.objects.get(server_type=server_type.lower()).server_type_id)
		Server.objects.create(
			host=host,
			port=int(port),
			username=username,
			password=password,
			username_api=username_api,
			password_api=password_api,
			port_api=int(port_api),
			protocal_api=protocal_api,
			server_type_id=server_type_id,
			file_path_root=file_path_root,
			description=description,
			)
		return redirect('/server/server_list')

# 删除服务器
@method_decorator(auth_login_required, name='dispatch')
class ServerDeleteView(View):
	def get(self, request):
		host = request.GET.get('host')
		server_type = request.GET.get('server_type')
		server_type_id = int(ServerType.objects.get(server_type=server_type.lower()).server_type_id)
		Server.objects.filter(host=host,server_type_id=server_type_id).delete()
		return redirect('/server/server_list')
		
# 编辑服务器
@method_decorator(auth_login_required, name='dispatch')
class ServerUpdateView(View):
	def get(self, request):
		host = request.GET.get('host')
		server_type = request.GET.get('server_type')
		server_type_id = ServerType.objects.get(server_type=server_type).server_type_id
		server = Server.objects.get(server_type_id=server_type_id, host=host)
		context = {'server': server, 'server_type': server_type}
		return render(request, 'server_update.html', context)

	def post(self, request):
		host = request.POST.get('host', '')
		port = request.POST.get('port', 0)
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		username_api = request.POST.get('username_api', '')
		password_api = request.POST.get('password_api', '')
		port_api = request.POST.get('port_api', 0)
		protocal_api = request.POST.get('protocal_api', '')
		file_path_root = request.POST.get('file_path_root', '')
		description = request.POST.get('description', '')
		server_type = request.POST.get('server_type', '')
		try:
			server_type_id = ServerType.objects.get(server_type=server_type).server_type_id
			obj = Server.objects.get(server_type_id=server_type_id, host=host)
			obj.host = host
			obj.port = int(port)
			obj.username = username
			obj.username_api = username_api
			obj.port_api = int(port_api)
			obj.protocal_api = protocal_api
			obj.file_path_root = file_path_root
			obj.description = description
			if password != '':
				obj.password = password
			else:
				data_encrypter = DataEncrypter()
				password = data_encrypter.decrypt(data=obj.password)
				obj.password = password
			if password_api != '':
				obj.password_api = password_api
			else:
				data_encrypter = DataEncrypter()
				password_api = data_encrypter.decrypt(data=obj.password_api)
				obj.password_api = password_api
			obj.save()
		except Exception as e:
			logging.error(e)
		return redirect('/server/server_list')