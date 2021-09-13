# coding=utf8

import logging
import threading

from app.docker.container import Container
from app.supervisor.process import Process
from app.server.models import Server

#重写Thread模块, 多线程支持获取返回值
class MyThread(threading.Thread):
	def __init__(self,func,args=()):
		super(MyThread,self).__init__()
		self.func = func
		self.args = args
	def run(self):
		self.result = self.func(*self.args)
	def get_result(self):
		try:
			# 如果子线程不使用join方法，此处可能会报没有self.result的错误
			return self.result
		except Exception:
			return None

# 获取所有服务器上的container信息，返回container列表
def get_container_lists(servers):
	container_list = []
	t_list = []
	results = []
	for server in servers:
		t = MyThread(Server.get_container_list, args=(server,))
		t_list.append(t)
	for t in t_list:
		t.start()
	for t in t_list:
		t.join()
		results.append(t.get_result())
	for result in results:
		for container in result:
			container_list.append(container)
	return (container_list)

# 获取所有服务器上的process信息，返回process列表
def get_process_lists(servers):
	process_list = []
	t_list = []
	results = []
	for server in servers:
		t = MyThread(Server.get_process_list, args=(server,))
		t_list.append(t)
	for t in t_list:
		t.start()
	for t in t_list:
		t.join()
		results.append(t.get_result())
	for result in results:
		for process in result:
			process_list.append(process)
	return (process_list)

# 获取所有服务器上的process信息，返回process列表
def get_job_lists(servers):
	job_list = []
	t_list = []
	results = []
	for server in servers:
		t = MyThread(Server.get_job_list, args=(server,))
		t_list.append(t)
	for t in t_list:
		t.start()
	for t in t_list:
		t.join()
		results.append(t.get_result())
	for result in results:
		for job in result:
			job_list.append(job)
	return (job_list)
	
