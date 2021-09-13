# coding=utf8

import requests
from app.utils.data_encrypter import DataEncrypter

# Jenkins的Job对象
class Job:
	host = ''
	host_port_api = ''
	host_username_api = ''
	host_password_api = ''
	host_protocal_api = ''
	name = ''

	# 触发任务构建
	def job_build_now(self, job_opt):
		data_encrypter = DataEncrypter()
		self.host_password_api =  data_encrypter.decrypt(data=self.host_password_api)
		jenkins_url_job_build_now = (self.host_protocal_api + '://'+ self.host + ':' 
			+ self.host_port_api + '/job/' + self.name + '/' + job_opt)
		response_build_result = requests.post(
			jenkins_url_job_build_now, 
			auth=(self.host_username_api, self.host_password_api))
		return (response_build_result)