## config.py

import os

# path_info
tmp_path = '/tmp'

# lines_for_view
lines_for_view = 10000

# page_info
page_size_default = 10

# db_info
db_engine = 'mysql'
db_host = '172.16.0.26'
db_port = 3306
db_user = 'root'
db_password = '111111'
db_name = 'mmanager'

# secret_info
key_data_encrypter = 'maxdSNxI_bHsKomtjGcJJWpHYbHdKQYh3Y_tygwZ_QM='

# 容器部署时，使用环境变量设置MySQL数据库信息
if (os.environ.get('db_host')) != None:
	db_host = os.environ.get('db_host')

if (os.environ.get('db_port')) != None:
	db_port = os.environ.get('db_port')

if (os.environ.get('db_user')) != None:
	db_user = os.environ.get('db_user')

if (os.environ.get('db_password')) != None:
	db_password = os.environ.get('db_password')