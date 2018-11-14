# -*- coding: utf-8 -*-
__author__ = 'ma'

from django.db import models

import xmlrpc.client, docker, logging, time 

from .common_func import get_time_stamp

# Create your models here.

# docker服务器模型
class Docker_Server(models.Model):
	hostname = models.CharField(max_length=50, verbose_name=u"主机名", unique=True)
	ip = models.GenericIPAddressField(u"主机IP", max_length=15)
	port = models.IntegerField(u'dockerAPI端口')
	username = models.CharField(max_length=50, verbose_name=u"docker用户名", default='', blank=True)
	password = models.CharField(max_length=50, verbose_name=u"docker密码", default='', blank=True)
	def __str__(self):
		return self.hostname

	# 获取docker api连接函数
	def get_docker_client(self):
		docker_client = docker.DockerClient(base_url='tcp://%s:%d' % (self.ip, self.port),version='1.21')
		return docker_client

	# 获取全部容器列表函数
	def get_all_container_info(self):
		try:
			docker_client = self.get_docker_client()
			container_infos = docker_client.containers.list(all=1)
			return container_infos
		except Exception as e:
			logging.error(e)
			return None 

	# 容器操作函数
	def container_opt(self, container_id, container_opt):
		docker_client = self.get_docker_client()
		if container_opt == 'start':
			docker_client.containers.get(container_id).start()
			return True
		if container_opt == 'stop':
			docker_client.containers.get(container_id).stop()
			return True
		if container_opt == 'restart':
			docker_client.containers.get(container_id).restart()
			return True

	# 容器日志获取
	def tail_container_log(self, container_id):
		log_list = []
		func_tail_log = self.get_docker_client().containers.get(container_id).logs
		log = func_tail_log(tail=20)
		log = log.decode()
		for log_line in log.split('\n'):
			time_stamp = get_time_stamp()
			log_line = '[' + time_stamp + ']--' + log_line
			log_list.append(log_line)
		return (log_list)

# supervisor服务器模型
class Supervisor_Server(models.Model):
	hostname = models.CharField(max_length=50, verbose_name=u"主机名", unique=True)
	ip = models.GenericIPAddressField(u"主机IP", max_length=15)
	port = models.IntegerField(u'supervisorRPC端口')
	username = models.CharField(max_length=50, verbose_name=u"supervisor用户名", default='', blank=True)
	password = models.CharField(max_length=50, verbose_name=u"supervisor密码", default='', blank=True)

	def __str__(self):
		return self.hostname

	# 获取supervisor的rpc接口函数
	def get_rpc_proxy(self):
		rpc_proxy = xmlrpc.client.ServerProxy('http://%s:%s@%s:%d/RPC2' % (self.username, self.password, self.ip, self.port))
		return rpc_proxy

	# 获取supervisor服务器上的进程列表函数
	def get_all_process_info(self):
		try:
			rpc_proxy = self.get_rpc_proxy()
			process_infos = rpc_proxy.supervisor.getAllProcessInfo()
			return process_infos
		except Exception as e:
			logging.error(e)
			process_infos = None
			return process_infos 

	# 启动指定supervisor管理的进程
	def start_process(self, supervisor_app):
		rpc_proxy = self.get_rpc_proxy()
		if self.check_status(supervisor_app, 0): # 0为状态码，表示app处于STOPPED状态 
			return rpc_proxy.supervisor.startProcess(supervisor_app)
		return True

	# 停止指定supervisor管理的进程
	def stop_process(self, supervisor_app):
		rpc_proxy = self.get_rpc_proxy()
		if self.check_status(supervisor_app, 10, 20): # 10为状态码，表示app处于STARTING状态，20表示app处于RUNNING状态 
			return rpc_proxy.supervisor.stopProcess(supervisor_app)
		return True

	# 重启指定supervisor管理的进程
	def restart_process(self, supervisor_app):
		rpc_proxy = self.get_rpc_proxy()
		if self.check_status(supervisor_app, 0):
			return rpc_proxy.supervisor.startProcess(supervisor_app)
		if self.check_status(supervisor_app, 10, 20):
			rpc_proxy.supervisor.stopProcess(supervisor_app)
			return rpc_proxy.supervisor.startProcess(supervisor_app)
		return True

	# 检查指定supervisor管理的进程状态
	def check_status(self, supervisor_app, *args):
		rpc_proxy = self.get_rpc_proxy()
		process_info = rpc_proxy.supervisor.getProcessInfo(supervisor_app)
		state = process_info.get('state')
		if state not in args:
			return False
		return True

	# supervisor管理的进程操作入口
	def supervisor_app_opt(self,supervisor_app, supervisor_opt):
		if supervisor_opt == 'start':
			self.start_process(supervisor_app)
			return True
		if supervisor_opt == 'stop':
			self.stop_process(supervisor_app)
			return True
		if supervisor_opt == 'restart':
			self.restart_process(supervisor_app)
			return True

	# supervisor管理的进程日志获取
	def tail_supervisor_app_log(self, supervisor_app):
		log_list = []
		offset = 0
		func = self.get_rpc_proxy().supervisor.tailProcessLog
		log, offset, ret = func(supervisor_app, offset, 2000)
		logging.error (log)
		for log_line in log.split('\n'):
			time_stamp = get_time_stamp()
			log_line = '[' + time_stamp + ']--' + log_line
			log_list.append(log_line)
		return (log_list)
