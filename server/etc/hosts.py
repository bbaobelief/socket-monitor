#!/usr/bin/env python
# -*- coding: utf-8 -*-
from templates import *

h1 = LinuxGenericServices()
h1.hostname = 'zheng'
h1.ip_address = '192.168.10.22'
h1.port = 22
h1.os = 'centos 5.5'

h2 = WindowsGenericServices()
h2.hostname = 'zhengfuqiang'
h2.ip_address = '192.168.8.187'
h2.port = 3389
h2.os = 'win8.1'

host_list = [h1,h2]

if __name__ == "__main__":
    del h2.os
    print h1.os,h2.os