# coding=utf8

import configparser
from django.conf import settings

# 获取配置文件位置，读取配置文件信息
CONF_DIR=(settings.BASE_DIR+'/config')
config = configparser.ConfigParser()
config.read(CONF_DIR+'/config.ini' ,encoding="utf-8")

# 配置文件类，读取配置文件，转化为json格式保存在config_info变量中
class ConfigInfo:
	config_info = {}
	def __init__(self):
		for section in config.sections():
			self.config_info[section] = {}
			for option in config.options(section):
				self.config_info[section][option] = config.get(section, option)