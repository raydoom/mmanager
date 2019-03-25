# -*- coding: utf-8 -*-
__author__ = 'ma'

from django.db import models
import paramiko, logging, re

from .container import Container
from .process import Process
from ..utils.common_func import exec_command_over_ssh


class ServerType(models.Model):
	server_type = models.CharField(max_length=50, verbose_name=u"server type", unique=True)
	def __str__(self):
		return self.server_type

class Server(models.Model):
	hostname = models.CharField(max_length=50, verbose_name=u"hostname", unique=True)
	ip = models.GenericIPAddressField(u"server ip", max_length=15)
	port = models.IntegerField(u'ssh port')
	username = models.CharField(max_length=50, verbose_name=u"ssh username", default='', blank=True)
	password = models.CharField(max_length=50, verbose_name=u"ssh password", default='', blank=True)
	description = models.CharField(max_length=128, verbose_name=u"description", default='', blank=True)
	server_type = models.ManyToManyField(ServerType)

	def __str__(self):
		return self.hostname
	# 获取容器列表
	def get_container_list(self):
		container_list = []
		cmd = 'docker ps -a | grep -v IMAGE'
		stdout = exec_command_over_ssh(self.ip, self.port, self.username, self.password, cmd)
		container_infos = stdout.decode().split('\n')
		for i in range(0,len(container_infos)-1):
			container_info = re.split('  +', container_infos[i])
			for j in range(0, len(container_infos[i])):
				 container = Container()
				 container.host_ip = self.ip 
				 container.host_port = self.port
				 container.container_id = container_info[0]
				 container.image = container_info[1]
				 container.command = container_info[2]
				 container.created = container_info[3]
				 container.status = container_info[4]
				 if 'up' in container.status.lower():
				 	container.statename = 'running'
				 if 'exited' in container.status.lower():
				 	container.statename = 'exited'
				 container.port = container_info[5]
				 container.name = container_info[-1]
				 if container_info[-1] == '':
				 	container.name = container_info[-2]
			container_list.append(container)
		return (container_list)

	# 获取supervisor进程列表
	def get_process_list(self):
		process_list = []
		cmd = 'supervisorctl status'
		stdout = exec_command_over_ssh(self.ip, self.port, self.username, self.password, cmd)
		process_infos = stdout.decode().split('\n')
		for i in range(0,len(process_infos)-1):
			process_info = re.split('  +', process_infos[i])
			for j in range(0, len(process_infos[i])):
				 process = Process()
				 process.host_ip = self.ip 
				 process.host_port = self.port
				 process.name = process_info[0]
				 process.statename = process_info[1]
				 process.description = process_info[2]
			process_list.append(process)
		return (process_list)
