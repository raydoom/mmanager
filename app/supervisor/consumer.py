# coding=utf8

import json
import threading
from channels.generic.websocket import WebsocketConsumer
from app.server.models import Server
from app.server.models import ServerType
from app.supervisor.process import Process
from app.utils.common_func import auth_login_required
from app.utils.common_func import log_record
from app.utils.common_func import param_to_dict
from app.utils.common_func import stop_thread
from app.utils.common_func import send_data_over_websocket_via_channels

# 获取supervisor程序的日志websocket
class ProcessLogConsumer(WebsocketConsumer):
	def connect(self):
		print ('channels 打开')
		print(self.scope.get('query_string').decode())
		# 连接时触发
		self.accept()
		param_dict = param_to_dict(self.scope.get('query_string').decode())
		host = param_dict.get('host')
		host_port = param_dict.get('host_port')
		process_name = param_dict.get('process_name')
		server_type_id = ServerType.objects.get(server_type='supervisor').server_type_id
		server = Server.objects.get(server_type_id=server_type_id, host=host, port=host_port)
		process = Process()
		process.host = server.host
		process.host_port = server.port
		process.host_username = server.username
		process.host_password = server.password
		process.process_name = process_name				
		self.channel = process.tail_process_logs()
		# 为每个websocket连接开启独立线程
		self.t = threading.Thread(target=send_data_over_websocket_via_channels, args=(self,))
		self.t.start()

	def disconnect(self, code):
		# 关闭连接时触发
		print ('channels 关闭')
		# 结束相应的线程
		try:
			stop_thread(self.t)
		except Exception as e:
			print(e)



