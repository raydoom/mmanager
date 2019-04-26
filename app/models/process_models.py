# coding=utf8

from django.db import models

# 容器信息模型
class ProcessModel(models.Model):
	host_ip = models.CharField((max_length=128)
	host_port = models.IntegerField()
	host_username = models.CharField(max_length=128)
	host_password =models.CharField(max_length=128)
	statename = models.CharField(max_length=128)
	name = models.CharField(max_length=128)
	description = models.CharField(max_length=128)