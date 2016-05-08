 #!D:\Python34\python.exe
# -*- coding: utf-8 -*-

'ab_try 程序的主程序'

__author__ = 'litter_zhang'

from ab_input import input_order
from settings import DEFAULT_HTTP_SCHEME, DEFAULT_HTTP_PORT
from ab_request import AB_REQUEST

if __name__=='__main__':
	#程序循环部分
	while True:
		suc, url, params = input_order()

		if suc:
			url_req = ''
			url_req += url['http'] or DEFAULT_HTTP_SCHEME
			url_req += url['host']
			url_req += ':' + (url['port'] or DEFAULT_HTTP_PORT)
			url_req += '/' + (url['path'] or '')

			print('正在测试 %s \n' % url['url'])

			request_ab = AB_REQUEST(*(url_req, ), **params)
			request_ab.start()

		else:
			print('输入指令有错误！')