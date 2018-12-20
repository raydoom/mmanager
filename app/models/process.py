# -*- coding: utf-8 -*-
__author__ = 'ma'

import paramiko


class Process:
	host_ip = ''
	host_port = 22
	host_username = ''
	host_password = ''
	host_port = 22
	statename = ''
	name = ''
	description = ''


	def supervisor_app_opt(self, supervisor_opt):
		cmd = 'supervisorctl ' +  supervisor_opt + ' ' + self.name
		try:
			ssh_client = paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh_client.connect(self.host_ip, self.host_port, self.host_username, self.host_password)
			std_in, std_out, std_err = ssh_client.exec_command(cmd)
			ssh_client.close()
			return (std_in, std_out, std_err)
		except Exception as e:
			logging.error(e)
			return None