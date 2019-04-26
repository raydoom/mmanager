# coding=utf8
__author__ = 'ma'

import time, os, logging, paramiko, multiprocessing, threading, re

from ..models.action_log_models import Action_Log
from django.shortcuts import render, redirect


# 获取格式化的当前时间
def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp

# 将时间戳转换为格式化的时间
def TimeStampToTime(timestamp):
	timeStruct = time.localtime(timestamp)
	return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

# 定义格式化日志的函数
def format_log(log):
	return '<div><a style="font-size:14px;">%s</a></div>' % (log,)

# 定义登陆状态控制器装饰器函数，如果未登录，则跳转到登录页面
def auth_controller(func):
	def wrapper(request,*args,**kwargs):
		if not request.session.get("islogin"):
			return redirect("/login/")
		return  func(request,*args, **kwargs)
	return wrapper

# 获取文件夹列表信息
def get_dir_info(path):
	dir_infos = [{'file_name': '..', 'isdir': 1},]	
	for dir_name in os.listdir(path):
		dir_info = {}
		filePath = path + dir_name
		fsize = os.path.getsize(filePath)
		if float(fsize) > 1024: # 判断文件大小并加相应的单位
			fsize = '%.2f'%(float(fsize)/1024)
			if float(fsize) > 1024:
				fsize = '%.2f'%(float(fsize)/1024)
				if float(fsize) > 1024:
					fsize = '%.2f'%(float(fsize)/1024)
					fsize = str(fsize) + ' GB'
				else:
					fsize = str(fsize) + ' MB'
			else:
				fsize = str(fsize) + ' KB'
		else:
			fsize = str(fsize) +' Bytes'

		mtime = os.path.getmtime(filePath)
		if os.path.isdir(filePath):
			dir_info['isdir'] = 1
		else:
			dir_info['isdir'] = 0
		dir_info['file_name'] = dir_name
		dir_info['file_size'] = fsize
		dir_info['mtime'] = TimeStampToTime(mtime)
		dir_infos.append(dir_info)
	return (dir_infos)

# 获取文件lines_per_page行的内容
def get_file_contents(dist, lines_per_page, page, filter_keyword):
	file = dist
	total_pages = 1
	contents_list = []
	try:
		with open(file, 'r' , encoding='utf-8' ) as file_to_read: # 
			if filter_keyword != '':
				line_filtered = []
				lines = file_to_read.readlines()
				lines_reversed = lines[::-1] #对读取到的行进行反序排列
				for i in range(0,len(lines_reversed)):
					if filter_keyword in lines_reversed[i]:
						line_filtered.append(lines_reversed[i])
				if len(line_filtered) == 0: # 如果结果为空，直接返回
					return ([], 0)
				if lines_per_page > len(line_filtered):
					lines_per_page = len(line_filtered)
				line_end = page*lines_per_page
				if page*lines_per_page >= len(line_filtered):
					line_end = len(line_filtered) 
				for i in range((page-1)*lines_per_page, line_end):
					contents_list.append(line_filtered[i])
				total_pages = (len(line_filtered)//lines_per_page) + 1				
			else:
				lines = file_to_read.readlines()
				if len(lines) == 0: # 如果结果为空，直接返回
					return ([], 0)
				if lines_per_page > len(lines):
					lines_per_page = len(lines)
				lines_reversed = lines[::-1] #对读取到的行进行反序排列
				line_end = page*lines_per_page
				if page*lines_per_page >= len(lines):
					line_end = len(lines) 
				for i in range((page-1)*lines_per_page, line_end):
					contents_list.append(lines_reversed[i])
				total_pages = (len(lines)//lines_per_page) + 1
	except Exception as e:
		logging.error(e)
		contents_list = ['Can not open file']	
	return (contents_list, total_pages)


# 记录日志函数
def log_record(log_user, log_detail):
	return (Action_Log.objects.create(log_user=log_user, log_detail=log_detail))

# ssh远程执行命令
def exec_command_over_ssh(ip='', port='22', username='', password='', cmd=''):
	try:
		ssh_client = paramiko.SSHClient()
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_client.connect(ip, port, username, password)
		std_in, std_out, std_err = ssh_client.exec_command(cmd)
		std_out = std_out.read()
		ssh_client.close()
		return (std_out)
	except Exception as e:
		logging.error(e)
		return None

# 获取paramiko的channel.exec_command对象
def get_channel_over_ssh(ip='', port='22', username='', password='', cmd=''):
	try:
		ssh_client = paramiko.SSHClient()
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_client.connect(ip, port, username, password)
		# open channel pipeline
		transport = ssh_client.get_transport()
		channel = transport.open_session()
		channel.get_pty()
		# out command into pipeline
		channel.exec_command(cmd)
		return channel
	except Exception as e:
		logging.error(e)
		return None 

# 将日志发送到websocket目标页面
def send_data_over_websocket(request, channel):
	while True:
		try:
			if request.websocket.is_closed(): # 检测客户端心跳，如果客户端关闭，则停止读取和发送日志
				print ('websocket is closed')
				channel.close()
				break
			if channel.recv_ready():
				recvfromssh = channel.recv(16371)
				log = recvfromssh.decode("utf-8" ,"ignore").encode("utf-8")
				request.websocket.send(log)
			request.websocket.send('')
			time.sleep(0.5)
		except Exception as e:
			logging.error(e)

# 发送容器shell的输出结果到web页面
def shell_output_sender(request, channel):
	while True:
		if request.websocket.is_closed(): # 检测客户端心跳，如果客户端关闭，则停止读取和发送日志
			print ('websocket is closed')
			channel.close()
			break
		if channel.recv_ready():
			recvfromssh = channel.recv(16371)
			request.websocket.send(recvfromssh)
		time.sleep(0.1)

# 接受页面输入并发送到容器shell
def shell_input_reciever(request, channel):
	while True:
		if request.websocket.is_closed(): # 检测客户端心跳，如果客户端关闭，则停止读取和发送日志
			print ('websocket is closed')
			channel.close()
			break
		for msg in request.websocket:
			cmd = msg.decode()
			channel.send(cmd)
