# -*- coding: utf-8 -*-

from django.db import models

# 权限表
class Permission(models.Model):
	title = models.CharField(verbose_name='标题', max_length=32)
	url = models.CharField(verbose_name='含正则的URL', max_length=128)

	def __str__(self):
		return self.title

# 角色
class Role(models.Model):
	title = models.CharField(verbose_name='角色名称', max_length=32)
	permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

	def __str__(self):
		return self.title

# 对自带的user模型进行扩展
class User_Info(models.Model):
	username = models.CharField("用户名", max_length=128, blank=False, unique=True)
	password = models.CharField("密码", max_length=128, blank=False)
	email = models.CharField("邮箱", max_length=128, blank=True)
	is_superuser = models.BooleanField("是否超级用户", blank=False)
	description = models.CharField("描述", max_length=128, blank=True)
	roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='Role', blank=True)

	def __str__(self):
		return self.username