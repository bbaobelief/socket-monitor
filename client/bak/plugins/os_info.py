#!/usr/bin/env python
# coding=utf8
import socket

def Get_Ostype():
    import os
    sys = os.name
    if sys == 'nt':
        return 'windows'
    elif sys == 'posix':
        return 'linux'
    else:
        return 'Unkwon'

def Get_Hostname():
    hostname = socket.gethostname()
    return hostname

def Get_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.baidu.com', 0))                               
    return s.getsockname()[0]

if __name__ == '__main__':
    info = {'hostname':Get_Hostname(),'ip':Get_IP(),'type':Get_Ostype()}
    print info