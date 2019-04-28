# coding=utf8

from django.db import models

# 进程信息模型
class ProcessInfo(models.Model):
	process_info_id = models.BigAutoField(primary_key=True)
	host = models.CharField(max_length=128)
	host_port = models.IntegerField()
	statename = models.CharField(max_length=128)
	name = models.CharField(max_length=128)
	description = models.CharField(max_length=128)
	current_user_id = models.IntegerField()
	class Meta:
		ordering = ['process_info_id']
		db_table = "app_process_info"