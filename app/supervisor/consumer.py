from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.consumer import SyncConsumer
import threading

from app.server.models import Server
from app.server.models import ServerType
from app.supervisor.process import Process
from app.utils.common_func import auth_login_required
from app.utils.common_func import log_record
from app.utils.common_func import stop_thread
from app.utils.common_func import send_data_over_websocket_via_channels
import asyncio

import time

class ProcessLog(WebsocketConsumer):
	t_dict = {}
	def connect(self):
		print ('channels 打开')
		print(self.scope.get('query_string').decode())
		# 连接时触发
		self.accept()
		# host = request.GET.get('host')
		# host_port = int(request.GET.get('host_port'))
		# process_name = request.GET.get('process_name')
		# server_type_id = ServerType.objects.get(server_type='supervisor').server_type_id
		# server = Server.objects.get(server_type_id=server_type_id, host=host, port=host_port)
		# process = Process()
		# process.host = server.host
		# process.host_port = server.port
		# process.host_username = server.username
		# process.host_password = server.password
		# process.process_name = process_name
		host = '172.16.0.121'
		host_port = 22
		process_name = 'box-agent'
		server_type_id = ServerType.objects.get(server_type='supervisor').server_type_id
		server = Server.objects.get(server_type_id=server_type_id, host=host, port=host_port)
		process = Process()
		process.host = server.host
		process.host_port = server.port
		process.host_username = server.username
		process.host_password = server.password
		process.process_name = process_name				
		channel = process.tail_process_logs()
		# 为每个websocket连接开启独立线程
		t = threading.Thread(target=send_data_over_websocket_via_channels, args=(self,channel))
		t.start()
		self.t_dict[self] = t
		# asyncio.run(send_data_over_websocket_via_channels(self,channel))

	def disconnect(self, code):
		# 关闭连接时触发
		print ('channels 关闭')
		# 结束相应的线程
		stop_thread(self.t_dict[self])
		# 从线程字典中删除
		del self.t_dict[self]

	def receive(self, text_data=None, bytes_data=None):
		# 收到消息后触发
		# 前端页面使用send()发送数据给websocket，由该函数处理
		# 真个ChatConsumer类会将所有接收到的消息加上一个"聊天"的前缀发送给客户端
		text_data_json = json.loads(text_data)
		message = "聊天:"+text_data_json["message"]
		self.send(text_data=json.dumps({"message":message}))
		
	def send_message(self, event):
		self.send(text_data=json.dumps({
			"message": event["message"]
		}))

def _async_raise(tid, exctype):
	"""raises the exception, performs cleanup if needed"""
	tid = ctypes.c_long(tid)
	if not inspect.isclass(exctype):
		exctype = type(exctype)
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
	if res == 0:
		raise ValueError("invalid thread id")
	elif res != 1:
		# """if it returns a number greater than one, you're in trouble,
		# and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
		raise SystemError("PyThreadState_SetAsyncExc failed")

