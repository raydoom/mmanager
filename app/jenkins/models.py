# coding=utf8
__author__ = 'ma'

from django.db import models

from app.utils.common_func import get_time_stamp

import jenkins, logging, time 


# jenkins服务器模型
class JenkinsServer(models.Model):
	hostname = models.CharField(max_length=50, verbose_name=u"主机名", unique=True)
	ip = models.GenericIPAddressField(u"主机IP", max_length=15)
	port = models.IntegerField(u'jenkins端口')
	apiversion = models.CharField(max_length=50, verbose_name=u"API版本", default='1.21', blank=True)
	username = models.CharField(max_length=50, verbose_name=u"jenkins用户名", default='', blank=True)
	password = models.CharField(max_length=50, verbose_name=u"jenkins密码", default='', blank=True)
	description = models.CharField(max_length=128, verbose_name=u"描述", default='', blank=True)
	class Meta:
		ordering = ['id']
		db_table = "app_jenkins_server"
	def __str__(self):
		return self.hostname

	def get_jenkins_server(self):
		jenkins_server = jenkins.Jenkins('http://%s:%d' %(self.ip, self.port) ,username=self.username, password=self.password)
		return (jenkins_server)

	# 获取jenkins的jobs列表
	def get_all_jobs_list(self):
		try:
			jenkins_server = self.get_jenkins_server()
			all_jobs_list = jenkins_server.get_all_jobs()
			for job in all_jobs_list:
				job['host_ip'] = self.ip
				job['host_port'] = self.port
			return (all_jobs_list)
		except Exception as e:
			logging.error(e)
			return None

	# 触发job构建
	def send_build_job(self, job_name):
		jenkins_server = self.get_jenkins_server()
		return (jenkins_server.build_job(job_name))