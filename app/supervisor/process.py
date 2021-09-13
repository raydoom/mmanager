# coding=utf8

import paramiko
from app.utils.common_func import exec_command_over_ssh, get_channel_over_ssh


# Process容器对象，supervisor管理的进程
class Process:
	host = ''
	host_port = 22
	host_username = ''
	host_password = ''
	statename = ''
	name = ''
	description = ''

	# process操作，启动，停止，重启
	def process_opt(self, process_opt):
		cmd = 'supervisorctl ' +  process_opt + ' ' + self.name
		stdout = exec_command_over_ssh(self.host, self.host_port, self.host_username, self.host_password, cmd)
		return (stdout)

	# 查看process控制台日志
	def tail_process_logs(self):
		cmd = 'supervisorctl tail -f ' + self.process_name	
		channel = get_channel_over_ssh(self.host, self.host_port, self.host_username, self.host_password, cmd)
		return (channel)