# -*- coding: utf-8 -*-
__author__ = 'ma'

import paramiko

from ..utils.common_func import exec_command_over_ssh, get_channel_over_ssh


class Process:
	host_ip = ''
	host_port = 22
	host_username = ''
	host_password = ''
	statename = ''
	name = ''
	description = ''


	def process_opt(self, process_opt):
		cmd = 'supervisorctl ' +  process_opt + ' ' + self.name
		stdin, stdout, stderr = exec_command_over_ssh(self.host_ip, self.host_port, self.host_username, self.host_password, cmd)
		return (stdin, stdout, stderr)

	def tail_process_logs(self):
		cmd = 'supervisorctl tail -f ' + self.process_name	
		channel = get_channel_over_ssh(self.host_ip, self.host_port, self.host_username, self.host_password, cmd)
		return (channel)