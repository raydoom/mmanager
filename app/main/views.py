# coding=utf8

import os
import logging
import json
import configparser
from django.shortcuts import render
from django.views import View

# 主页
class IndexView(View):
	def get(self, request):
		return render(request, 'index.html')


