# coding=utf8

# 需要安装扩展模块 pip3 install cryptography

from cryptography.fernet import Fernet
from config import config

# key_data_encrypter
key_data_encrypter = config.key_data_encrypter

# 利用key对字符串加密和解密
class DataEncrypter():
	def __init__(self):
		self.key = key_data_encrypter.encode(encoding='utf8')
		self.encrypt_func = Fernet(self.key)

	# 加密函数
	def encrypt(self, data):
		data = data.encode(encoding='utf8')
		cipherdata = self.encrypt_func.encrypt(data)
		return cipherdata.decode(encoding='utf8')

	# 解密函数
	def decrypt(self, data):
		data = data.encode(encoding='utf8')
		plain_data = self.encrypt_func.decrypt(data)
		return plain_data.decode(encoding='utf8')


