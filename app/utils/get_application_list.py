# -*- coding: utf-8 -*-
__author__ = 'ma'

import logging, threading

from ..models.container import Container
from ..models.process import Process
from ..models.server import Server


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
			return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
		except Exception:
			return None

# 使用多线程连接不同服务器，获取container信息
def get_container_list(servers):
	container_list = []
	t_list = []
	results = []
	for server in servers:
		t = MyThread(Server.get_container_list, args=(server,))
		t_list.append(t)
		t.start()
	for t in t_list:
		t.join()
		results.append(t.get_result())
	for result in results:
		for container in result:
			container_list.append(container)
	return (container_list)

# 使用多线程连接不同服务器，获取process信息
def get_process_list(servers):
	process_list = []
	t_list = []
	results = []
	for server in servers:
		t = MyThread(Server.get_process_list, args=(server,))
		t_list.append(t)
		t.start()
	for t in t_list:
		t.join()
		results.append(t.get_result())
	for result in results:
		for process in result:
			process_list.append(process)
	return (process_list)









































# def get_container_list(servers):
# 	container_list = []
# 	cmd = 'docker ps -a | grep -v IMAGE'
# 	results = parallel_exec_cmd(servers, cmd)
# 	for result in results:
# 		container_infos = result.decode().split('\n')
# 		for i in range(0,len(container_infos)-1):
# 			container_info = re.split('  +', container_infos[i])
# 			for j in range(0, len(container_infos[i])):
# 				 container = Container()
# 				 #container.host_ip = self.ip 
# 				 #container.host_port = self.port
# 				 container.container_id = container_info[0]
# 				 container.image = container_info[1]
# 				 container.command = container_info[2]
# 				 container.created = container_info[3]
# 				 container.status = container_info[4]
# 				 if 'up' in container.status.lower():
# 				 	container.statename = 'running'
# 				 if 'exited' in container.status.lower():
# 				 	container.statename = 'exited'
# 				 container.port = container_info[5]
# 				 container.name = container_info[-1]
# 				 if container_info[-1] == '':
# 				 	container.name = container_info[-2]
# 			container_list.append(container)
# 	return (container_list)

# def get_process_list(servers):
# 	process_list = []
# 	cmd = 'supervisorctl status'
# 	stdout = exec_command_over_ssh(self.ip, self.port, self.username, self.password, cmd)
# 	process_lists = stdout.decode().split('\n')
# 	for i in range(0,len(process_lists)-1):
# 		process_info = re.split('  +', process_lists[i])
# 		for j in range(0, len(process_lists[i])):
# 			 process = Process()
# 			 process.host_ip = self.ip 
# 			 process.host_port = self.port
# 			 process.name = process_info[0]
# 			 process.statename = process_info[1]
# 			 process.description = process_info[2]
# 		process_list.append(process)
# 	return (process_list)