# coding=utf8

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from app.utils.config_info_formater import ConfigInfo

# 获取默认page_size大小
config = ConfigInfo()
page_size_default = int(config.config_info.get('page_info').get('page_size_default'))

# 列表分页函数
def paginator_for_list_view(object_list, page_num):
	paginator = Paginator(object_list, page_size_default)
	try:
		result_list = paginator.page(page_num)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		result_list = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		result_list = paginator.page(paginator.num_pages)
	return (result_list)