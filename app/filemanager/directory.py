# coding=utf8

import logging
from app.utils.common_func import exec_command_over_ssh

class Directory:
	def get_file_list(self, path='/tmp/'):
		try:
			cmd = 'ls -alh ' +  path
			stdout = exec_command_over_ssh(self.host, self.host_port, self.host_username, self.host_password, cmd)
			stdout = stdout.decode(encoding='utf8').split('\n')[2:-1]
			return (stdout)
		except Exception as e:
			logging.error(e)
			return []