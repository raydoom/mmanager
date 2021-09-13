# coding=utf8

from django.db import models

# 进程信息模型
class JobInfoCache(models.Model):
	job_info_cache_id = models.BigAutoField(primary_key=True)
	host = models.CharField(max_length=128)
	host_port_api = models.IntegerField()
	host_protocal_api = models.CharField(max_length=128)
	color = models.CharField(max_length=128)
	name = models.CharField(max_length=128)
	current_user_id = models.IntegerField()
	class Meta:
		ordering = ['job_info_cache_id']
		db_table = "app_job_info_cache"