# -*- coding: utf-8 -*-
__author__ = 'ma'

import time, os, logging

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

# 获取文件最后lines_per_page行的内容
def get_file_contents(dist, lines_per_page):
	file = dist
	contents_list = []
	try:
		with open(file, 'r' , encoding='utf-8' ) as file_to_read: # 
			lines = file_to_read.readlines()
			if lines_per_page > len(lines):
				lines_per_page = len(lines)
			lines_reversed = lines[::-1] #对读取到的行进行反序排列
			for i in range(0, lines_per_page):
				contents_list.append(lines_reversed[i])
	except Exception as e:
		logging.error(e)
		contents_list = ['Can not open file']	
	return (contents_list)


# 记录日志函数
def log_record(log_user, log_detail):
	return (Action_Log.objects.create(log_user=log_user, log_detail=log_detail))

