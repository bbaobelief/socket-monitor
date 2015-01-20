#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import socket
import time
from SocketServer import ThreadingTCPServer, StreamRequestHandler
from etc import redis_connector as redis

hostinfo = ['127.0.0.1','192.168.10.22','192.168.10.21','192.168.8.187']

result = {}

class MyStreamRequestHandlerr(StreamRequestHandler):
    # def setup(self):  
    #     self.request.settimeout(60)
    def handle(self):
        #判断主机是否有权限发送数据
        if self.client_address[0] in hostinfo:
            self.wfile.write('AllowConnection')
            #self.client_address是客户端的连接(host, port)的元组
            #print 'Connected from', self.client_address

            #接收客户端连接请求
            receivedData = self.rfile.readline().strip()
            #receivedData = self.request.recv(8192).strip()

            #主机资源信息存入mysql
            if receivedData == "SendMonitorData":
                #print "receive from (%r):%r" % (self.client_address, receivedData)
                self.wfile.write('ReadyToReceive')
                resource_data = json.loads(self.request.recv(8192))
                #print resource_data
            #主机状态信息存入redis
            elif receivedData == "SendStatusData":
                print "---------going to save data into redis....---done!!!"
                self.wfile.write('Allowsthereceiving')
                status_data = json.loads(self.request.recv(8192))
                status_data['host_check'] = time.time()
                
                #为每个服务添加检查时间
                status_data['result'][status_data['result'].keys()[0]]['check_time'] = time.time()
                
                #重新组合数据
                result[status_data['result'].keys()[0]] = status_data['result'].values()[0]
                status_data['result'] = result
                print "\033[42;1mdata from %s\033[0m" % self.client_address[0],'\n',status_data

                redis.r[self.client_address[0]] = json.dumps(status_data)
                print u'....write redis done....'
        else:
            self.wfile.write('Connectionrefused')
            print self.client_address[0],u'非法连接，已拒绝...'


    def finish(self):  
        self.request.close() 

if __name__ == "__main__":
    host = ""          #主机名
    port = 9999     #端口
    addr = (host, port)
    
    #ThreadingTCPServer从ThreadingMixIn和TCPServer继承
    #class ThreadingTCPServer(ThreadingMixIn, TCPServer): pass
    try:
        server = ThreadingTCPServer(addr, MyStreamRequestHandlerr)
        print "waiting for connection..."
        #启动服务监听
        server.serve_forever()
    except socket.error:
        print u'%s端口未释放...'%port


