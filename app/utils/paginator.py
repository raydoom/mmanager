# coding=utf8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 列表分页函数
def paginator_for_list_view(object_list, page_num):
	paginator = Paginator(object_list, 10)
	try:
		result_list = paginator.page(page_num)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		result_list = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		result_list = paginator.page(paginator.num_pages)
	return (result_list)