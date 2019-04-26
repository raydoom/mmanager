# coding=utf8

from django.db import models

# 容器信息模型
class ContainerModel(models.Model):
	host_ip = models.CharField()
	host_port = models.IntegerField()
	host_username = models.CharField(max_length=50)
	host_password =models.CharField(max_length=50)
	container_id = models.CharField(max_length=50)
	image = models.CharField(max_length=256)
	command = models.CharField(max_length=50)
	created = models.CharField(max_length=50)
	statename = models.CharField(max_length=50)
	status = models.CharField(max_length=50)
	port = models.CharField(max_length=256)
	name = models.CharField(max_length=50)