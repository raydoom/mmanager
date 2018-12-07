# -*- coding: utf-8 -*-
__author__ = 'ma'

from django.db import models

import xmlrpc.client, logging, time 

from ..utils.common_func import get_time_stamp


# supervisor服务器模型
class Supervisor_Server(models.Model):
	hostname = models.CharField(max_length=50, verbose_name=u"主机名", unique=True)
	ip = models.GenericIPAddressField(u"主机IP", max_length=15)
	port = models.IntegerField(u'supervisorRPC端口')
	apiversion = models.CharField(max_length=50, verbose_name=u"API版本", default='1.21', blank=True)
	username = models.CharField(max_length=50, verbose_name=u"supervisor用户名", default='', blank=True)
	password = models.CharField(max_length=50, verbose_name=u"supervisor密码", default='', blank=True)
	description = models.CharField(max_length=128, verbose_name=u"描述", default='', blank=True)

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
			for process_info in process_infos:
				process_info['host_ip'] = self.ip
				process_info['host_port']= self.port
			return process_infos
		except Exception as e:
			logging.error(e)
			return None 

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
	def tail_supervisor_app_log(self, supervisor_app, format_func):
		offset = 0
		func = self.get_rpc_proxy().supervisor.tailProcessLog
		secs = 0
		while secs < 60 :
			log, offset, ret = func(supervisor_app, offset, 2000)
			time.sleep(1)
			secs += 1
			for log_line in log.split('\n'):
				yield format_func(log_line)
