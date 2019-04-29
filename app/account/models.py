# coding=utf8

from django.db import models


# 用户
class UserInfo(models.Model):
	user_id = models.BigAutoField(primary_key=True)
	username = models.CharField(max_length=128, blank=False, unique=True)
	password = models.CharField(max_length=128, blank=False)
	email = models.CharField(max_length=128, blank=True)
	role = models.CharField(max_length=32, blank=True)
	description = models.CharField(max_length=128, blank=True)
	def __str__(self):
		return self.username
	class Meta:
		ordering = ['user_id']
		db_table = "app_user_info"