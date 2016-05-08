#!D:\Python34\python.exe
# -*- coding: utf-8 -*-

'ab_try 程序的输入部分，包括输入参数解析'

__author__ = 'litter_zhang'

import re

RE_INPUT_ORDER = r'^ab\s+(?P<params>(?:-\w\s+[^-][^\s]*\s+|-\w\s+)*)(?P<url>(?P<http>http://|https://){0,1}(?P<host>[^/|^:]+)(?::(?P<port>\d+)){0,1}(?P<path>/[\w|\d|\.|/]*){0,1})$'
RE_ORDER_PARAM = r'(?:(?:-(?P<key_2>\w)\s+(?P<value>[^-][^\s]*)\s+)|(?:-(?P<key_1>\w)\s+))'
RE_NUMBER = r'^\d+$'
RE_NONE = r'^$'
RE_AUTH = r'^[^\s]+:[^\s]+$'
RE_COOKIE = r'^[^\s]+\=[^\s]+$'
RE_HEADER = r'^[^\s]+:\s*[^\s]+$'
RE_POST_DATA = r'^[^\s]+=[^\s]+$'

#添加对应参数
def add_param(params, key, value):
	if key=='c' and re.match(RE_NUMBER, value):
		params['con_num'] = int(value)
	if key=='n' and re.match(RE_NUMBER, value):
		params['req_num'] = int(value)
	if key=='k' and re.match(RE_NONE, value):
		params['keep_alive'] = True
	if key=='d' and re.match(RE_NONE, value):
		params['show_table'] = False
	if key=='a' and re.match(RE_AUTH, value):
		params['base_auth'] = value
	if key=='C' and re.match(RE_COOKIE, value):
		params['cookies'] = params.get('cookies', []).append(value)
	if key=='H' and re.match(RE_HEADER, value):
		params['headers'] = params.get('headers', []).append(value.split(':'))
	if key=='P' and re.match(RE_POST_DATA, value):
		params_post_data = params.get('post_data', {})
		params_post_data[value.split('=')[0]] = value.split('=')[1]
		params['post_data'] = params_post_data
	return params


#解析输入指令的参数
def get_params(params_str):
	params = dict()

	rs = re.findall(RE_ORDER_PARAM, params_str)
	for r in rs:
		param_key = r[0] or r[2]
		param_val = r[1] or ''

		params = add_param(params, param_key.strip(), param_val.strip())
	return params

#输入程序，解析出所有的参数
def input_order():
	line = input('输入指令: ').strip()
	#line = 'ab -c 10 -n 100 -k -a hello:1882323 www.baidu.com'

	url_r = dict()
	suc_r = True
	params = dict()

	r = re.match(RE_INPUT_ORDER, line)
	if r:
		#指令的参数总的str
		input_params = r.group('params')
		#进行指令的参数解析
		params = get_params(input_params)

		input_url = r.group('url')
		input_http = r.group('http')
		input_host= r.group('host')
		input_port = r.group('port')
		input_path = r.group('path')

		url_r['url'] = input_url
		url_r['http'] = input_http
		url_r['host'] = input_host
		url_r['port'] = input_port
		url_r['path'] = input_path

	else:
		suc_r = False
	return suc_r, url_r, params


if __name__=='__main__':
	input_order()
