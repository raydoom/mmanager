# coding=utf8

from django.db import models


# 用户
class UserInfo(models.Model):
	user_id = models.BigAutoField(primary_key=True)
	username = models.CharField("用户名", max_length=128, blank=False, unique=True)
	password = models.CharField("密码", max_length=128, blank=False)
	email = models.CharField("邮箱", max_length=128, blank=True)
	is_superuser = models.BooleanField("是否超级用户", blank=False)
	description = models.CharField("描述", max_length=128, blank=True)
	def __str__(self):
		return self.username
	class Meta:
		managed = False
		ordering = ['user_id']
		db_table = "app_user_info"