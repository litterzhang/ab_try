# Apache Benchmark Try —— ab_try

----------

Apache Benchmark 的python模仿，实现功能如下：  
1. ab www.baidu.com: 向指定站点发送Http请求，默认请求100次，10个并发线程  
2. -n 100 : 发送请求的数量  
3. -c 10 : 并发的数量  
4. -k : 使用一个keep-alive会话发送所有的请求  
5. -d : 不显示请求发送时间百分比的表  
6. -a username:password : Basic Auth验证  
7. -C uuu=hhh : 可重复出现，请求附带的cookie  
8. -H uuu:hhh : 可重复出现，自定义的请求头部  
9. -P uuu=hhh : 可重复出现，POST方式请求，后面为POST提交的数据