# -*- coding: utf-8 -*-
__author__ = 'ma'

import paramiko

from ..utils.common_func import exec_command_over_ssh, get_channel_over_ssh


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
		stdout = exec_command_over_ssh(self.host_ip, self.host_port, self.host_username, self.host_password, cmd)
		return (stdout)

	def tail_container_logs(self):
		cmd = 'docker logs -f --tail=10 ' + self.container_id
		channel = get_channel_over_ssh(self.host_ip, self.host_port, self.host_username, self.host_password, cmd)
		return (channel)

