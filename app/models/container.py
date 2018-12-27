# -*- coding: utf-8 -*-
__author__ = 'ma'

import paramiko

from ..utils.common_func import exec_command_over_ssh, get_channel_over_ssh


# Container容器对象
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

	# 容器操作，启动，停止，重启
	def container_opt(self, container_opt):
		cmd = 'docker ' +  container_opt + ' ' + self.container_id
		stdout = exec_command_over_ssh(self.host_ip, self.host_port, self.host_username, self.host_password, cmd)
		return (stdout)

	# 查看容器控制台日志
	def tail_container_logs(self):
		cmd = 'docker logs -f --tail=10 ' + self.container_id
		channel = get_channel_over_ssh(self.host_ip, self.host_port, self.host_username, self.host_password, cmd)
		return (channel)

	# 获取容器shell
	def container_shell(self):
		sshclient = paramiko.SSHClient()
		sshclient.load_system_host_keys()
		sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		sshclient.connect(self.host_ip, self.host_port, self.host_username, self.host_password)
		channel = sshclient.invoke_shell(term='xterm')
		channel.settimeout(0)
		return (channel)