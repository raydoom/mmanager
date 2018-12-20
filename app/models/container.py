# -*- coding: utf-8 -*-
__author__ = 'ma'

import paramiko


class Container:
	host_ip = ''
	host_port = 22
	host_username = ''
	host_password = ''
	container_id = ''
	image = ''
	command = ''
	created = ''
	statename = ''
	status = ''
	port = ''
	name = ''

	def container_opt(self, container_opt):
		cmd = 'docker ' +  container_opt + ' ' + self.container_id
		print (cmd)
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
