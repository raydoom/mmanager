# -*- coding: utf-8 -*-
__author__ = 'ma'

from django.db import models

import xmlrpc.client, docker, logging, time 

from ..common_func import get_time_stamp

# Create your models here.

# docker服务器模型
class Docker_Server(models.Model):
	hostname = models.CharField(max_length=50, verbose_name=u"主机名", unique=True)
	ip = models.GenericIPAddressField(u"主机IP", max_length=15)
	port = models.IntegerField(u'dockerAPI端口')
	apiversion = models.CharField(max_length=50, verbose_name=u"API版本", default='1.21', blank=True)
	username = models.CharField(max_length=50, verbose_name=u"docker用户名", default='', blank=True)
	password = models.CharField(max_length=50, verbose_name=u"docker密码", default='', blank=True)
	def __str__(self):
		return self.hostname

	# 获取docker client连接函数
	def get_docker_client(self):
		docker_client = docker.DockerClient(base_url='tcp://%s:%d' % (self.ip, self.port), version=self.apiversion)
		return docker_client

	# 获取docker apiclient连接函数
	def get_docker_apiclient(self):
		docker_apiclient = docker.APIClient(base_url='tcp://%s:%d' % (self.ip, self.port), version=self.apiversion)
		return docker_apiclient

	# 获取全部容器列表函数
	def get_all_container_info(self):
		try:
			docker_client = self.get_docker_client()
			docker_apiclient = self.get_docker_apiclient()
			container_info_client = docker_client.containers.list(all=1)
			container_info_apiclient = docker_apiclient.containers(all=1)
			# 利用APIClient获取docker运行的时长，添加到容器信息中，字段为apistatus
			for container_api in container_info_apiclient:
				for container in container_info_client:
					if container.id == container_api['Id']:
						container.apistatus = container_api['Status']
			container_infos = container_info_client
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
	# def tail_container_log(self, container_id):
	# 	log_list = []
	# 	func_tail_log = self.get_docker_client().containers.get(container_id).logs
	# 	log = func_tail_log(tail=20)
	# 	log = log.decode()
	# 	for log_line in log.split('\n'):
	# 		time_stamp = get_time_stamp()
	# 		log_line = '[' + time_stamp + ']--' + log_line
	# 		log_list.append(log_line)
	# 	return (log_list)

	# 容器日志获取
	def tail_container_log(self, container_id, format_func):
		func_tail_log = self.get_docker_client().containers.get(container_id).logs
		log_old, log_new = '', ''
		secs = 0
		while secs < 60 :		
			log = func_tail_log(tail=15)
			log = log.decode()
			time.sleep(1)
			secs = secs+1
			log_old = log_new
			log_new = log
			for log_line in log.split('\n'):
				time_stamp = get_time_stamp()
				log_line = '[' + time_stamp + ']--' + log_line
				duplicate_flag = 0
				for log_old_line in log_old.split('\n'):
					log_old_line = '[' + time_stamp + ']--' + log_old_line
					if log_line == log_old_line:
						duplicate_flag = 1
				if duplicate_flag == 0:
					yield format_func(log_line)
