# coding=utf8

import logging, time 
from django.db import models

# 操作日志
class ActionLog(models.Model):
	action_log_id = models.BigAutoField(primary_key=True)
	log_time = models.DateTimeField(auto_now_add=True)
	log_user = models.CharField(max_length=50)
	log_detail = models.CharField(max_length=256)
	class Meta:
		ordering = ['action_log_id']
		db_table = "app_action_log"