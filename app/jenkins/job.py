# coding=utf8
__author__ = 'ma'

import requests


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
		jenkins_url_job_build_now = self.host_protocal_api + '://'+ self.host + ':' + self.host_port_api + '/job/' + self.name + '/' + job_opt
		response_build_result = requests.post(jenkins_url_job_build_now, auth=(self.host_username_api, self.host_password_api))
		return (response_build_result)