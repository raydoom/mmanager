# coding=utf8
__author__ = 'ma'

from django.db import models
import paramiko, logging, re, requests

from app.docker.container import Container
from app.supervisor.process import Process
from app.jenkins.job import Job
from app.utils.common_func import exec_command_over_ssh

# 主机类型
class ServerType(models.Model):
	server_type_id = models.BigAutoField(primary_key=True)
	server_type = models.CharField(max_length=50, unique=True)
	class Meta:
		ordering = ['server_type_id']
		db_table = "app_server_type"
	def __str__(self):
		return self.server_type

# 主机
class Server(models.Model):
	server_id = models.BigAutoField(primary_key=True)
	host = models.CharField(max_length=50)
	port = models.IntegerField(default=0)
	username = models.CharField(max_length=50, default='', blank=True)
	password = models.CharField(max_length=50, default='', blank=True)
	username_api = models.CharField(max_length=50, default='', blank=True)
	password_api = models.CharField(max_length=50, default='', blank=True)	
	port_api = models.IntegerField(default=0)
	protocal_api = models.CharField(max_length=50, default='', blank=True)
	description = models.CharField(max_length=128, default='', blank=True)
	server_type_id = models.IntegerField()
	class Meta:
		ordering = ['server_id']
		db_table = "app_server"
	def __str__(self):
		return self.host

	# 获取容器列表
	def get_container_list(self):
		container_list = []
		cmd = 'docker ps -a | grep -v IMAGE'
		stdout = exec_command_over_ssh(self.host, self.port, self.username, self.password, cmd)
		container_infos = stdout.decode().split('\n')
		for i in range(0,len(container_infos)-1):
			container_info = re.split('  +', container_infos[i])
			for j in range(0, len(container_infos[i])):
				 container = Container()
				 container.host = self.host 
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
		stdout = exec_command_over_ssh(self.host, self.port, self.username, self.password, cmd)
		process_infos = stdout.decode().split('\n')
		for i in range(0,len(process_infos)-1):
			process_info = re.split('  +', process_infos[i])
			for j in range(0, len(process_infos[i])):
				 process = Process()
				 process.host = self.host 
				 process.host_port = self.port
				 process.name = process_info[0]
				 process.statename = process_info[1]
				 process.description = process_info[2]
			process_list.append(process)
		return (process_list)

	# 获取job列表
	def get_job_list(self):
		job_list = []
		jenkins_job_list_url = self.protocal_api + '://' + self.host + ':' + str(self.port_api) + '/api/json'
		jenkins_response = requests.get(jenkins_job_list_url, auth=(self.username_api, self.password_api))
		job_info = jenkins_response.json().get('jobs')
		for i in range(0,len(job_info)):
			job = Job()
			job.host=self.host
			job.host_port_api=self.port_api
			job.host_protocal_api=self.protocal_api
			job.name=job_info[i].get('name')
			job.color=job_info[i].get('color')
			job_list.append(job)
		return (job_list)

# 主机信息缓存，用于查询主机列表时生成分页
class ServerInfoCache(models.Model):
	server_info_cache_id = models.BigAutoField(primary_key=True)
	server_id = models.IntegerField()
	host = models.CharField(max_length=50)
	port = models.IntegerField()
	port_api = models.IntegerField()
	protocal_api = models.CharField(max_length=50, default='', blank=True)
	description = models.CharField(max_length=128, default='', blank=True)
	status = models.CharField(max_length=50, default='', blank=True)
	server_type = models.CharField(max_length=50)
	current_user_id = models.IntegerField()
	class Meta:
		ordering = ['server_info_cache_id']
		db_table = "app_server_info_cache"
	def __str__(self):
		return self.host