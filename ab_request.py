 #!D:\Python34\python.exe
# -*- coding: utf-8 -*-

'ab_try 程序的发送请求部分'

__author__ = 'litter_zhang'

import requests
import base64
from urllib.parse import urlparse
from threadpool import ThreadPool, makeRequests
from requests.auth import AuthBase

from settings import *


#定制请求的Header
class AB_REQUEST_H(AuthBase):
	def __init__(self, base_auth=None, cookies=[], headers=[]):
		self._base_auth = base64.encodestring(bytes(base_auth or '', 'utf-8'))
		self._cookies = cookies
		self._headers = headers

	def __call__(self, req):

		if self._base_auth:
			req.headers['Authorization'] = 'Basic {0}'.format(self._base_auth)
		req.headers['Cookie'] = ';'.join(self._cookies)
		for header in self._headers:
			req.headers[header[0]] = header[1]

		return req


#整个请求的类
class AB_REQUEST:
	def __init__(self, url, req_num=DEFAULT_REQUEST_NUM, con_num=DEFAULT_CONCURRENCY_NUM, \
		keep_alive=DEFAULT_KEEP_ALIVE, show_table=DEFAULT_DISPLAY_TABLE, base_auth=None, \
		cookies=[], headers=[], post_data=None, timeout_c=DEFAULT_TIMEOUT_CONNECT, timeout_r=DEFAULT_TIMEOUT_READ):
		self._url = url

		self._show_table = show_table

		#请求会话信息
		self._session = requests.session()
		self._keep_alive = keep_alive

		#定制请求头部
		self._auth = AB_REQUEST_H(base_auth=base_auth, cookies=cookies, headers=[])

		#POST信息
		self._post = post_data

		#并发线程信息
		self._pool_num = con_num
		self._pool = ThreadPool(con_num)

		#请求任务信息
		self._tasks_num = req_num
		self._tasks = makeRequests(self.make_a_request, [url for i in range(self._tasks_num)], self.end_a_request)

		#请求超时设置
		self._timeout_c = timeout_c
		self._timeout_r = timeout_r

		#统计信息
		self._cnt_complete = 0
		self._cnt_success = 0
		self._cnt_fail = 0

		self._time = list()
		self._document_len = list()
		self._status = dict()

	#获取测试服务器的信息
	def get_server_msg(self):
		status = -1
		time = 0
		doc_len = 0
		
		try:
			if self._post:
				r = self._session.post(self._url, data=self._post, auth=self._auth, timeout=(self._timeout_c, self._timeout_r))
			else:
				r = self._session.get(self._url, auth=self._auth, timeout=(self._timeout_c, self._timeout_r))
			
			r.encoding = 'utf-8'

			print('------------------------')
			print('Server Software: %s' % r.headers['Server'])
			print('Document Type: %s' % r.headers['Content-Type'])
			print('Document Length: %d' % len(r.text))
			print('------------------------\n')
		except Exception as e:
			print('Server Error: %s' % e)
		
	#发送一次请求
	def make_a_request(self, url):
		status = -1
		time = 0
		doc_len = 0
		
		try:
			if self._post:
				r = self._session.post(self._url, data=self._post, auth=self._auth, timeout=(self._timeout_c, self._timeout_r))
			else:
				r = self._session.get(self._url, auth=self._auth, timeout=(self._timeout_c, self._timeout_r))

			r.encoding = 'utf-8'
			status = r.status_code
			time = r.elapsed.total_seconds()
			doc_len = len(r.text)
		except Exception as e:
			print('Server Error: %s' % e)
			status = -1

		res = [status, time or 0, doc_len or 0]
		return res

	#发送请求结束统计
	def end_a_request(self, req, res):
		status = res[0]
		time = res[1]
		doc_len = res[2]

		self._status[status] = self._status.get(status, 0) + 1
		self._time.append(time)
		self._document_len.append(doc_len)

		if status!=-1:
			self._cnt_success += 1
			self._cnt_complete += 1
		else:
			self._cnt_fail += 1
			self._cnt_complete += 1


	#获取发送请求时的会话session
	@property
	def session(self):
		if self._keep_alive:
			return self._session
		else:
			return requests.session()
	
	def analyse(self):
		print('------------------------')
		print('完成请求: %d' % self._cnt_complete)
		print('成功请求: %d' % self._cnt_success)
		print('失败请求: %d' % self._cnt_fail)
		print('------------------------\n')

		print('请求响应总大小: %d' % sum(self._document_len))

		time_avg = sum(self._time)/len(self._time)
		print('请求平均响应时间: %.3fms' % (time_avg*1000))
		print('------------------------\n')

		for status, cnt in self._status.items():
			print('status %s 出现 %d 次: ' % (status, cnt))
		print('------------------------\n')

		time_sort = sorted(self._time, key=lambda x: x)

		if self._show_table:
			print('10%%请求在%.3fms内完成: ' % (time_sort[int(len(time_sort)*0.1)]*1000))
			print('20%%请求在%.3fms内完成: ' % (time_sort[int((len(self._time)-1)*0.2)]*1000))
			print('30%%请求在%.3fms内完成: ' % (time_sort[int((len(self._time)-1)*0.3)]*1000))
			print('40%%请求在%.3fms内完成: ' % (time_sort[int((len(self._time)-1)*0.4)]*1000))
			print('50%%请求在%.3fms内完成: ' % (time_sort[int((len(self._time)-1)*0.5)]*1000))
			print('60%%请求在%.3fms内完成: ' % (time_sort[int((len(self._time)-1)*0.6)]*1000))
			print('70%%请求在%.3fms内完成: ' % (time_sort[int((len(self._time)-1)*0.7)]*1000))
			print('80%%请求在%.3fms内完成: ' % (time_sort[int((len(self._time)-1)*0.8)]*1000))
			print('90%%请求在%.3fms内完成: ' % (time_sort[int((len(self._time)-1)*0.9)]*1000))
			print('100%%请求在%.3fms内完成: ' % (time_sort[len(self._time)-1]*1000))


	#开始发送请求任务
	def start(self):
		self.get_server_msg()
		[self._pool.putRequest(req) for req in self._tasks]
		self._pool.wait()
		self.analyse()