# -*- coding: utf-8 -*-
__author__ = 'ma'

from django.db import models

import logging, time 

from ..common_func import get_time_stamp


class User_Log(models.Model):
	log_time = models.DateTimeField(auto_now_add=True)
	log_user = models.CharField(max_length=50)
	log_detail = models.CharField(max_length=256)

		