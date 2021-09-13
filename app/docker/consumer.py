# coding=utf8

import json
import time 
import threading
from channels.generic.websocket import WebsocketConsumer
from app.server.models import Server
from app.server.models import ServerType
from app.docker.container import Container
from app.utils.common_func import auth_login_required
from app.utils.common_func import log_record
from app.utils.common_func import param_to_dict
from app.utils.common_func import stop_thread
from app.utils.common_func import send_data_over_websocket_via_channels
from app.utils.common_func import shell_output_sender_via_channels
from app.utils.common_func import shell_input_reciever_via_channels

# 实时查看容器日志websocket
class ContainerLogConsumer(WebsocketConsumer):
	def connect(self):
		print ('channels 打开')
		print(self.scope.get('query_string').decode())
		# 连接时触发
		self.accept()
		param_dict = param_to_dict(self.scope.get('query_string').decode())
		host = param_dict.get('host')
		host_port = int(param_dict.get('host_port'))
		container_id = param_dict.get('container_id')
		container_name = param_dict.get('container_name')
		server_type_id = ServerType.objects.get(server_type='docker').server_type_id
		server = Server.objects.get(server_type_id=server_type_id, host=host, port=host_port)
		container = Container()
		container.host = server.host
		container.host_port = server.port
		container.host_username = server.username
		container.host_password = server.password
		container.container_id = container_id
		self.channel = container.tail_container_logs()
		# 为每个websocket连接开启独立线程
		self.t = threading.Thread(target=send_data_over_websocket_via_channels, args=(self,))
		self.t.start()

	def disconnect(self, code):
		# 关闭连接时触发
		print ('channels 关闭')
		# 结束相应的线程
		stop_thread(self.t)

# 容器命令行websocket
class ContainerConsoleConsumer(WebsocketConsumer):
	t_dict = {}
	def connect(self):
		print ('channels 打开')
		print(self.scope.get('query_string').decode())
		# 连接时触发
		self.accept()
		param_dict = param_to_dict(self.scope.get('query_string').decode())
		host = param_dict.get('host')
		host_port = int(param_dict.get('host_port'))
		container_id = param_dict.get('container_id')
		container_name = param_dict.get('container_name')
		server_type_id = ServerType.objects.get(server_type='docker').server_type_id
		server = Server.objects.get(server_type_id=server_type_id, host=host, port=host_port)
		container = Container()
		container.host = server.host
		container.host_port = server.port
		container.host_username = server.username
		container.host_password = server.password
		container.container_id = container_id
		self.channel = container.container_shell()
		init_cmd = 'docker exec -it ' + container_id + ' bash\n'
		self.channel.send(init_cmd)
		time.sleep(1)
		init_recieve = self.channel.recv(16371).decode()
		# 不支持bash的容器，用sh进行连接
		if 'executable file not found' in init_recieve:
			init_cmd = 'docker exec -it ' + container_id + ' sh\n'
			self.channel.send(init_cmd)
			time.sleep(1)
			init_recieve = self.channel.recv(16371).decode()
		# 连接错误，返回
		if 'Error' in init_recieve:
			logging.error(init_recieve)
			request.websocket.send(' container is not running or not support shell... ')
			time.sleep(60)
			return 0
		self.channel.send('\n')
		# th_sender为将shell输出发送到web端线程
		self.th_sender = threading.Thread(target=shell_output_sender_via_channels, args=(self,))
		self.th_sender.start()

	def receive(self, text_data=None, bytes_data=None):
		# th_reciever为接收用户输入线程 
		self.th_reciever = threading.Thread(target=shell_input_reciever_via_channels, args=(self,text_data))
		self.th_reciever.start()

	def disconnect(self, code):
		# 关闭连接时触发
		print ('channels 关闭')
		# 结束相应的线程
		try:
			stop_thread(self.th_sender)
			stop_thread(self.th_reciever)
		except Exception as e:
			print(e)



		



