# -*- coding: utf-8 -*-
__author__ = 'ma'

import time

from django.shortcuts import render, redirect

# 获取格式化的时间
def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp


# 定义格式化日志的函数
def format_log(log):
	return '<div>%s</div>' % (log,)

# 定义登陆状态控制器，如果未登录，则跳转到登录页面
def auth_controller(func):
	def wrapper(request,*args,**kwargs):
		if not request.session.get("islogin"):
			return redirect("/login/")
		return  func(request,*args, **kwargs)
	return wrapper