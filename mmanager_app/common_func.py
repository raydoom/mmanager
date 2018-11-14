# -*- coding: utf-8 -*-
__author__ = 'ma'

import time

# 获取格式化的时间
def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp

# 定义格式化日志的函数
def format_log(log):
	return '<div>%s</div>' % (log,)