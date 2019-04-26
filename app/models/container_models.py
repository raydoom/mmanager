# coding=utf8

from django.db import models

# 容器信息模型，存储每次实时获取到的container数据，用于实现分页
class ContainerModel(models.Model):
	host_ip = models.CharField()
	host_port = models.IntegerField()
	host_username = models.CharField(max_length=128)
	host_password =models.CharField(max_length=128)
	container_id = models.CharField(max_length=128)
	image = models.CharField(max_length=128)
	command = models.CharField(max_length=128)
	created = models.CharField(max_length=128)
	statename = models.CharField(max_length=128)
	status = models.CharField(max_length=128)
	port = models.CharField(max_length=128)
	name = models.CharField(max_length=128)
	current_user_id = models.IntegerField()