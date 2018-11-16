# -*- coding: utf-8 -*-
__author__ = 'ma'

import time, os, logging

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
	return '<div>%s</div>' % (log,)

# 定义登陆状态控制器装饰器函数，如果未登录，则跳转到登录页面
def auth_controller(func):
	def wrapper(request,*args,**kwargs):
		if not request.session.get("islogin"):
			return redirect("/login/")
		return  func(request,*args, **kwargs)
	return wrapper

# 获取文件夹列表信息
def get_dir_info(path):
	print (path)
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
	print (dir_infos)
	return (dir_infos)

# 获取文件最后10000字符的内容
def get_file_contents(path, file_name):
	file = path + file_name
	print('file_to_read:', file)
	contents_list = []
	try:
		with open(file, 'rb' ) as file_to_read: # 以只读，二进制打开文件，只有二进制才能支持函数seek(0, 2)从末尾读
			bytes_to_read = 100000 # 需要读取的字节数
			bytes_counter = file_to_read.seek(0, 2)
			if bytes_counter > bytes_to_read:
				offset = file_to_read.tell() - bytes_to_read
			else:
				offset = 0
			file_to_read.seek(offset, 0)
			lines = file_to_read.readlines()
			for line in lines:
				try:
					line = line.decode(encoding = "utf-8") # 将读取到的二进制转为文本
					contents_list.append(line)
				except Exception as e:
					logging.error(e)
					contents_list = ['Not a text file']
	except Exception as e:
		logging.error(e)
		contents_list = ['Can not open file']
	return (contents_list)

