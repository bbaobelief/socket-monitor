#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Filename   : CheckClient.py
# Revision   : 1.0
# Date       : 2014/11/14
# Author     : ZhengFuqiang
# Email      : zhengfuqiang@gyyx.cn
# Description: The client checks
# Notes      : This plugin uses the "" command
# ---------------------------------------------------------------------------
# 返回数据格式如下: {'log_time': '15:27:13', 'app_id': 6258, 'result': {'cpu': {'status': 0, 'iowait': '0.33'}, 'memory': {'status': 0, 'MemTotal': '1026932'}}}

import socket
import time,json
import ConfigParser
from plugins import cpu,memory

HOST = 'localhost'
PORT = 9999
BUF=1024
TIMEOUT=10
PWD='/root/zhengfuqiang/py/socket/Monitor/Client'

def w_log(string):
    fp=open('%s/logs/check.log'%PWD,'ab')
    fp.write('%s  %s\n'%(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),string))
    fp.close()

def readconfig():
    # reading the configuration file
    cf=ConfigParser.ConfigParser()
    try:
        cf.read('%s/config.ini'%PWD)
    except:
        w_log('Open config.ini error')
        sys.exit(1)
    return cf

def checkinfo():
    # check info
    result = {}
    cp = readconfig()
    for i in cp.sections():
        if i == 'global':
            ip1=cp.get(i,'IPADDR')
            ip2=cp.get(i,'IPADDR2')
        elif i == 'info':
            o = cp.options("info")
            #print 'options:', o
            for c in o:
                if cp.get(i,c) == 'True':
                    #print c+' = '+cp.get(i,c)
                    try:
                        #print eval("%s.monitor()"%c)
                        #result.append({c:eval("%s.monitor()"%c)})
                        result[c] = eval("%s.monitor()"%c)
                    except NameError,e:
                        #print e
                        pass
                else:
                    pass
        else:
            try:
                app_id = int(i) 
            except ValueError:
                w_log('%s is not a valid serverid'%i)
                continue
            #print i,ip1
    checkinfo = {'log_time':time.strftime('%Y-%m-%d %X'),'app_id':app_id,'result':result}
    return checkinfo

def send_status_data(action,status_data):
    # send monitor data to  server side 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HOST, PORT))
    if action == 'SendMonitorData':
        print '----SendMonitorData----'
        s.send('SendMonitorData')
        server_confirmation = s.recv(1024)
        if server_confirmation == "ReadyToReceive":
                s.sendall( status_data)

        data = s.recv(1024)
        print  data
        s.close()

status_dic = {'hostname': 'zhengfuqiang','check_time': '15:27:13', 'app_id': 6258, 'result': {'cpu': {'status': 0, 'iowait': '0.33'}, 'memory': {'status': 0, 'MemTotal': '1026932'}}}
send_status_data('SendMonitorData',json.dumps(status_dic))


# def main():
#     return checkinfo()

# if __name__ == "__main__":
#     print main()