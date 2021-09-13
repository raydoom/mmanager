# coding=utf8

from django.db import models

# 容器信息模型，存储每次实时获取到的container数据，用于实现分页
class ContainerInfoCache(models.Model):
	container_info_cache_id = models.BigAutoField(primary_key=True)
	host = models.CharField(max_length=128)
	host_port = models.IntegerField()
	container_id = models.CharField(max_length=128)
	image = models.CharField(max_length=128)
	command = models.CharField(max_length=128)
	created = models.CharField(max_length=128)
	statename = models.CharField(max_length=128)
	status = models.CharField(max_length=128)
	port = models.CharField(max_length=128)
	name = models.CharField(max_length=128)
	current_user_id = models.IntegerField()
	class Meta:
		ordering = ['container_info_cache_id']
		db_table = "app_container_info_cache"