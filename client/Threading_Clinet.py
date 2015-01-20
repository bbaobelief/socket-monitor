#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import json
import time
import threading
from plugins_api import *
import sys

HOST = '192.168.10.22'
PORT = 9999
result = {}

def send_status_data(action,status_data):
    #建立socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #建立连接
    try:
        s.connect((HOST, PORT))
        constatus = s.recv(1024)
        if constatus == 'AllowConnection':
            if action == 'SendMonitorData':
                print '----SendMonitorData----'
                #发送连接请求
                s.sendall(action+'\n')
                #接收回复确认
                request_reply = s.recv(1024)
                if request_reply == "ReadyToReceive":
                    s.sendall(status_data)
                    print  status_data
                s.close()
            elif action == 'SendStatusData':
                print '----SendStatusData----'
                #发送连接请求
                s.sendall(action+'\n')
                #接收回复确认
                request_reply = s.recv(1024)
                if request_reply == "Allowsthereceiving":
                    s.sendall(status_data)
                    print  status_data
                s.close()
        else:
            print  u'木有权限，拒绝连接%s'%constatus
            sys.exit(0)
    except Exception,e:
        print e,';  Try to reconnect...'

def run(service_config):
    """ 每个服务起一个检查进程"""
    status = {}
    service_name,interval,plugin_name = service_config
    res = eval(plugin_name)()
    #result[service_name] = res   #汇总数据

    status[service_name] = res
    #print status
    service_data = {'hostname': 'zheng', 'app_id': 1000, 'result': status}
    #print  "\033[32m %s \033[0m" %service_data
    send_status_data('SendStatusData',json.dumps(service_data))
    return service_data


if __name__ == '__main__': 
    host_config = {'load':[30,'load_info',0],'cpu':[60,'cpu_info',0],'memory':[120,'memory_info',0]}
    while True:
        for k,v in host_config.items():
            interval,plugin_name,last_run = v
            if (time.time() - last_run) >= interval:
                t = threading.Thread(target=run,args=((k,interval,plugin_name), ))
                t.start()
                host_config[k][2] = time.time()
            else:
                next_run = interval - (time.time() - last_run)
                #print '------------->',int(next_run)
        time.sleep(1) 





