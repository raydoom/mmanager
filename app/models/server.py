# -*- coding: utf-8 -*-
__author__ = 'ma'

from django.db import models
import paramiko, logging, re

from .container import Container
from .process import Process


class ServerType(models.Model):
	server_type = models.CharField(max_length=50, verbose_name=u"主机类型", unique=True)
	def __str__(self):
		return self.server_type

class Server(models.Model):
	hostname = models.CharField(max_length=50, verbose_name=u"主机名", unique=True)
	ip = models.GenericIPAddressField(u"主机IP", max_length=15)
	port = models.IntegerField(u'ssh端口')
	username = models.CharField(max_length=50, verbose_name=u"ssh用户名", default='', blank=True)
	password = models.CharField(max_length=50, verbose_name=u"ssh密码", default='', blank=True)
	description = models.CharField(max_length=128, verbose_name=u"描述", default='', blank=True)
	server_type = models.ManyToManyField(ServerType)

	def __str__(self):
		return self.hostname

	def get_ssh_connect(self, cmd):
		try:
			ssh_client = paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			print (self.ip)
			ssh_client.connect(self.ip, self.port, self.username, self.password)
			std_in, std_out, std_err = ssh_client.exec_command(cmd)
			ssh_client.close()
			return (std_in, std_out, std_err)
		except Exception as e:
			logging.error(e)
			return None 

	def get_container_list(self):
		container_list = []
		try:
			ssh_client = paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh_client.connect(self.ip, self.port, self.username, self.password)
			std_in, std_out, std_err = ssh_client.exec_command('docker ps -a | grep -v IMAGE')
			for line in std_out:
				container_infos = line.strip("\n")
				container_info = re.split('  +', container_infos)
				for i in range(0,len(container_info)):
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
			ssh_client.close()
			return container_list
		except Exception as e:
			logging.error(self.ip,e)
			return None 

	def get_process_list(self):
		process_list = []
		try:
			ssh_client = paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh_client.connect(self.ip, self.port, self.username, self.password)
			std_in, std_out, std_err = ssh_client.exec_command('supervisorctl status')
			for line in std_out:
				process_infos = line.strip("\n")
				process_info = re.split('  +', process_infos)
				for i in range(0,len(process_info)):
				 	process = Process()
				 	process.host_ip = self.ip 
				 	process.host_port = self.port
				 	process.name = process_info[0]
				 	process.statename = process_info[1]
				 	process.description = process_info[2]
				process_list.append(process)
			ssh_client.close()
			return process_list
		except Exception as e:
			logging.error(e)
			return None 